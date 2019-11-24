import logging

from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions
from rest_framework.exceptions import PermissionDenied

from .models import Token

logger = logging.getLogger(__name__)

UserModel = get_user_model()


def get_token_from_request(request):
    """
    Extract the token from the ``Authorization`` header if the prefix is ``"Bearer"``, or return ``None`` otherwise.
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
    if not auth_header or auth_header[0].lower() != TokenAuthentication.keyword.lower():
        return None

    return auth_header[1]


def get_valid_token(token: str):
    """
    Get the Token object associated with the given ``token`` string, and check the expiration date before returning it.
    Expired tokens are deleted and ``None`` is returned in all failure cases (expired, not found, etc).
    """
    if token:
        try:
            t = Token.objects.get(key=token)
            if timezone.now() <= t.expiration:
                return t
            else:
                t.delete()
        except Token.DoesNotExist:
            pass

    return None


def clear_tokens(user, except_token=None):
    tokens = Token.objects.filter(user=user)
    if except_token:
        tokens = tokens.exclude(key=except_token)

    tokens.delete()


def logout(request, target_token=None, all_tokens=False):
    """
    Delete the authorization token from the request, and then logout from
    ``django-allauth``, if installed, or directly from django if not.

    If ``target_token`` is given, that token is deleted instead, and logout of ``request``
    is only performed if its token matches ``target_token``.

    If ``all_tokens`` is True, all tokens associated with ``request.user``, except the token currently in use,
    are deleted. It is not valid to pass both ``all_tokens`` and ``target_token``.

    Tokens can only be deleted if they are owned by ``request.user``.

    Returns True if the targeted token(s) were deleted, or if no user was logged in to begin with.
    """
    assert not (target_token and all_tokens)
    req_token = get_token_from_request(request)
    do_logout = False
    if not getattr(request.user, 'is_authenticated', True):
        return True

    if all_tokens:
        clear_tokens(request.user, except_token=req_token)
        do_logout = False
    else:
        if not target_token:
            target_token = req_token

        token_obj = get_valid_token(target_token)
        if token_obj:
            if token_obj.user != request.user:
                logger.warning("%s attempts to delete token owned by %s!", str(request.user), str(token_obj.user))
                raise PermissionDenied(_("Token owner mismatch."))

            token_obj.delete()
            do_logout = target_token == req_token

    if do_logout:
        del request.META['HTTP_AUTHORIZATION']

        try:
            # noinspection PyUnresolvedReferences
            from allauth.account.adapter import get_adapter
            get_adapter(request).logout(request)
        except ImportError:
            django_logout(request)


class TokenBackend(object):
    """Django authentication backend."""

    def authenticate(self, request, token=None):
        user = None
        try:
            user, token_obj = TokenAuthentication().authenticate_credentials(token)
            assert token_obj.key == token
        except exceptions.AuthenticationFailed:
            pass

        return user

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class TokenAuthentication(authentication.TokenAuthentication):
    """Django REST Framework authenticator."""
    keyword = 'Bearer'
    model = Token

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if token and timezone.now() > token.expiration:
            try:
                token.delete()
            except Exception:
                pass

            raise exceptions.AuthenticationFailed(_('Expired token.'))

        return user, token
