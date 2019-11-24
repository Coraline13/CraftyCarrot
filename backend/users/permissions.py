from allauth.account.adapter import get_adapter
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsNotStaff(BasePermission):
    message = "Don't use your admin account on the site."

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if request.user.is_staff:
            raise PermissionDenied(IsNotStaff.message)

        return True


class IsOpenForSignup(BasePermission):
    message = _('Sign-up period is closed.')

    def has_permission(self, request, view):
        return super().has_permission(request, view) \
               and IsNotStaff().has_permission(request, view) \
               and get_adapter(request).is_open_for_signup(request)


class IsNotAuthenticated(BasePermission):
    message = _('You cannot perform this action while authenticated.')

    def has_permission(self, request, view):
        return super().has_permission(request, view) \
               and not IsAuthenticated().has_permission(request, view)
