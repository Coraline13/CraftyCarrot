import copy

from allauth.account import app_settings as allauth_settings
from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from ..serializers import TokenSerializer, UserSerializer, password_min_length


class RegisterInputSerializer(UserSerializer):
    # confirmation_query_args = serializers.DictField(child=serializers.CharField(max_length=2083))

    class Meta(UserSerializer.Meta):
        fields = ('email', 'first_name', 'last_name')
        read_only_fields = ()

        if not settings.SET_PASSWORD_ON_EMAIL_CONFIRMATION:
            fields = fields + ('password',)

        if allauth_settings.USERNAME_REQUIRED:
            fields = ('username',) + fields


class LoginInputSerializer(UserSerializer):
    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        # remove unique constraint from email, otherwise serialiezr validation will fail
        # we are trying to log in, not register a new account
        email_validators = extra_kwargs.get('email', {}).get('validators', [])
        email_validators[:] = [v for v in email_validators if not isinstance(v, UniqueValidator)]
        return extra_kwargs

    class Meta(UserSerializer.Meta):
        fields = ('email', 'password')
        read_only_fields = ()
        extra_kwargs = copy.deepcopy(UserSerializer.Meta.extra_kwargs)


class ConfirmEmailInputSerializer(UserSerializer):
    key = serializers.CharField()

    class Meta(UserSerializer.Meta):
        fields = ('key',)
        read_only_fields = ()

        if settings.SET_PASSWORD_ON_EMAIL_CONFIRMATION:
            fields = fields + ('password',)


class LogoutInputSerializer(Serializer):
    token = serializers.CharField(required=False, default='',
                                  help_text="Invalidate a specific session. Invalidates the current session if null.")
    all = serializers.BooleanField(required=False, default=False,
                                   help_text="Invalidate all sessions except the current session.")


class RequestPasswordResetInputSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('email',)
        read_only_fields = ()


class ResetPasswordInputSerializer(UserSerializer):
    uidb36 = serializers.CharField(max_length=64)
    key = serializers.CharField(max_length=64)

    class Meta(UserSerializer.Meta):
        fields = ('password', 'uidb36', 'key')
        read_only_fields = ()


class ChangePasswordInputSerializer(Serializer):
    old_password = serializers.CharField(min_length=password_min_length(), write_only=True)
    new_password = serializers.CharField(min_length=password_min_length(), write_only=True)


class TokenResponseSerializer(Serializer):
    token = TokenSerializer(read_only=True, help_text='Authentication token, if a user was logged in by this request.')


class UserTokenResponseSerializer(TokenResponseSerializer):
    user = UserSerializer(read_only=True, help_text='The user logged in by this request, if any.')
    email = serializers.EmailField(read_only=True, help_text='E-mail address of the affected user, if applicable. '
                                                             'This is sent even if the user was not logged in.')
