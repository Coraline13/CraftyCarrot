import logging

from allauth.account import app_settings as allauth_settings
from allauth.account import signals
from allauth.account.forms import (
    ChangePasswordForm, LoginForm, ResetPasswordForm, ResetPasswordKeyForm, SetPasswordForm, SignupForm, UserTokenForm
)
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.utils import complete_signup, logout_on_password_change
from allauth.account.views import ConfirmEmailView, confirm_email
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import (
    AccountAdapter, clear_messages, form_valid_or_raise, handle_login_response, login_with_profile,
    map_serializer_to_form
)
from ..backends import clear_tokens, get_token_from_request, logout
from ..permissions import IsNotAuthenticated, IsOpenForSignup
from .serializers import (
    ChangePasswordInputSerializer, ConfirmEmailInputSerializer, LoginInputSerializer, LogoutInputSerializer,
    UserTokenResponseSerializer, RegisterInputSerializer, RequestPasswordResetInputSerializer,
    ResetPasswordInputSerializer, TokenResponseSerializer
)

logger = logging.getLogger(__name__)

User = get_user_model()


class RegisterAPIView(APIView):
    permission_classes = (IsNotAuthenticated, IsOpenForSignup)

    def permission_denied(self, request, message=None):
        raise PermissionDenied(detail=message)

    @swagger_auto_schema(
        operation_id='register', request_body=RegisterInputSerializer, responses={
            status.HTTP_200_OK: TokenResponseSerializer
        })
    def post(self, request):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        signup_data = dict(serializer.validated_data)
        confirmation_query_args = signup_data.pop('confirmation_query_args', {})
        email = signup_data.pop('email')
        signup_data['email'] = signup_data['email2'] = email
        if not settings.SET_PASSWORD_ON_EMAIL_CONFIRMATION:
            password = signup_data.pop('password')
            signup_data['password1'] = signup_data['password2'] = password

        email_verification = allauth_settings.EMAIL_VERIFICATION
        with transaction.atomic(), clear_messages(request):
            form = SignupForm(data=signup_data)
            if settings.SET_PASSWORD_ON_EMAIL_CONFIRMATION:
                form.fields.pop('password1', None)
                form.fields.pop('password2', None)

            form_valid_or_raise(form, {'password1': 'password', 'password2': None, 'email2': None})

            user = form.save(request=request)
            if email_verification != allauth_settings.EmailVerificationMethod.NONE and confirmation_query_args:
                user.extra_confirmation_data[AccountAdapter.CONFIRMATION_QUERY_ARGS] = confirmation_query_args
                user.save()

            response = complete_signup(request, user, email_verification, success_url=None)
            token = handle_login_response(response, user, allow_disabled=True)
            response_serializer = TokenResponseSerializer({'token': token})
            return Response(response_serializer.data)


class LoginAPIView(APIView):
    permission_classes = (IsNotAuthenticated,)

    @swagger_auto_schema(
        operation_id='login', request_body=LoginInputSerializer, responses={
            status.HTTP_200_OK: UserTokenResponseSerializer
        })
    def post(self, request):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_field = 'email'
        form_login = serializer.validated_data.get('email', '')
        if not form_login:
            form_login = serializer.validated_data.get('username', '')
            if form_login:
                login_field = 'username'

        login_data = {
            'login': form_login,
            'password': serializer.validated_data.get('password')
        }

        with transaction.atomic(), clear_messages(request):
            form = LoginForm(request=request, data=login_data)
            form_valid_or_raise(form, {'login': login_field})
            allauth_response = form.login(request)
            # commit transaction here because an implicit EmailConfirmation object may be created
            # as part of the allauth login process, and we want it to be saved

        with transaction.atomic(), clear_messages(request):
            user = getattr(form, 'user', None)
            token = handle_login_response(allauth_response, user, allow_disabled=False)
            profile = getattr(getattr(token, 'user', None), 'profile', None)
            response_serializer = UserTokenResponseSerializer({'token': token, 'profile': profile})
            response = Response(response_serializer.data)
            return response


class ConfirmEmailAPIView(APIView):
    permission_classes = (IsNotAuthenticated,)

    def _get_email_confirmation(self, key):
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            # noinspection PyTypeChecker
            queryset = ConfirmEmailView.get_queryset(self=None)
            email_confirmation = queryset.get(key=key.lower())
        return email_confirmation

    @swagger_auto_schema(
        operation_id='confirm_email', request_body=ConfirmEmailInputSerializer, responses={
            status.HTTP_200_OK: UserTokenResponseSerializer
        })
    def post(self, request):
        serializer = ConfirmEmailInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        key = serializer.validated_data.get('key')

        with transaction.atomic(), clear_messages(request):
            try:
                confirmation = self._get_email_confirmation(key=key)
                # mitigate the risk of login-on-confirm by only logging in on the first usage of the link
                auto_login = confirmation and confirmation.email_address and not confirmation.email_address.verified
                confirm_email(request, key=key)
            except (ObjectDoesNotExist, Http404):
                raise serializers.ValidationError(_('E-mail verification link is invalid or has expired. '
                                                    'To resend the link, try logging in.'))
            email = confirmation.email_address.email
            user = confirmation.email_address.user  # type: User
            user.extra_confirmation_data.pop(AccountAdapter.CONFIRMATION_QUERY_ARGS, {})

            if settings.SET_PASSWORD_ON_EMAIL_CONFIRMATION:
                if user.has_usable_password():
                    raise PermissionDenied('Password is already set')

                password_form_map = {'password1': 'password', 'password2': 'password'}
                password_form_input = map_serializer_to_form(serializer.validated_data, password_form_map)
                set_password_form = SetPasswordForm(user=user, data=password_form_input)
                form_valid_or_raise(set_password_form, password_form_map)
                set_password_form.save()
                # don't send password_set signal because request is not authenticated

            token, profile = None, None
            if auto_login and allauth_settings.LOGIN_ON_EMAIL_CONFIRMATION:
                token, profile = login_with_profile(request, user, allauth_settings.EmailVerificationMethod.NONE)

            user.save()
            response_serializer = UserTokenResponseSerializer({'token': token, 'profile': profile, 'email': email})
            return Response(response_serializer.data)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id='logout', request_body=LogoutInputSerializer, responses={
            status.HTTP_200_OK: 'Logged out succesfully.'
        })
    def post(self, request):
        serializer = LogoutInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get('token')
        all_tokens = serializer.validated_data.get('all_tokens')
        if all_tokens and token:
            raise serializers.ValidationError(_("Specific token cannot be invalidated when invalidating all tokens."))

        with transaction.atomic(), clear_messages(request):
            logout(request, target_token=token, all_tokens=all_tokens)
            response = Response({})
            return response


class RequestPasswordResetAPIView(APIView):
    permission_classes = (IsNotAuthenticated,)

    @swagger_auto_schema(
        operation_id='request_password_reset', request_body=RequestPasswordResetInputSerializer, responses={
            status.HTTP_200_OK: openapi.Response('Password reset initiated succesfully.')
        }
    )
    def post(self, request):
        serializer = RequestPasswordResetInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        with transaction.atomic(), clear_messages(request):
            form = ResetPasswordForm(data={'email': email})
            form_valid_or_raise(form)
            form.save(request=request)
            return Response({})


class ResetPasswordAPIView(APIView):
    permission_classes = (IsNotAuthenticated,)

    @swagger_auto_schema(
        operation_id='reset_password', request_body=ResetPasswordInputSerializer, responses={
            status.HTTP_200_OK: UserTokenResponseSerializer
        })
    def post(self, request):
        serializer = ResetPasswordInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb36 = serializer.validated_data.get('uidb36')
        key = serializer.validated_data.get('key')

        token_form_input = {'uidb36': uidb36, 'key': key}
        password_form_map = {'password1': 'password', 'password2': 'password'}
        password_form_input = map_serializer_to_form(serializer.validated_data, password_form_map)

        with transaction.atomic(), clear_messages(request):
            token_form = UserTokenForm(data=token_form_input)
            form_valid_or_raise(token_form)
            user = token_form.reset_user
            email = EmailAddress.objects.filter(user=user, email=user.email, verified=True).first()
            if not email:
                raise PermissionDenied(_("This account is pending e-mail address verification."))
            email = getattr(email, 'email', None)
            reset_form = ResetPasswordKeyForm(user=user, temp_key=key, data=password_form_input)
            form_valid_or_raise(reset_form, password_form_map)
            reset_form.save()
            signals.password_reset.send(sender=user.__class__, request=request, user=user)

            clear_tokens(user)
            token, profile = None, None
            if allauth_settings.LOGIN_ON_PASSWORD_RESET:
                token, profile = login_with_profile(request, user)

            response_serializer = UserTokenResponseSerializer({'token': token, 'profile': profile, 'email': email})
            return Response(response_serializer.data)


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id='change_password', request_body=ChangePasswordInputSerializer, responses={
            status.HTTP_200_OK: 'Password changed succesfully.'
        })
    def post(self, request):
        serializer = ChangePasswordInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_form_map = {'password1': 'new_password', 'password2': 'new_password', 'oldpassword': 'old_password'}
        change_form_input = map_serializer_to_form(serializer.validated_data, change_form_map)

        with transaction.atomic(), clear_messages(request):
            user = request.user
            if not user.has_usable_password():
                raise PermissionDenied(_("This account is disabled."))

            change_form = ChangePasswordForm(user=user, data=change_form_input)
            form_valid_or_raise(change_form, change_form_map)
            change_form.save()

            logout(request, all_tokens=True)  # logout all other sessions
            if allauth_settings.LOGOUT_ON_PASSWORD_CHANGE:
                # maybe logout current session too
                logout(request)
            logout_on_password_change(request, user)  # make allauth happy
            signals.password_changed.send(sender=user.__class__, request=request, user=user)
            return Response({})


class DeleteAccountAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id='delete_account', responses={
            status.HTTP_200_OK: 'Account deleted succesfully.'
        })
    def delete(self, request, *args, **kwargs):
        with transaction.atomic(), clear_messages(request):
            user = request.user
            logout(request, all_tokens=True)
            logout(request)
            user.delete()
            return Response({})
