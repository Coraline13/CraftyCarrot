from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission, IsAuthenticated

from users.permissions import IsNotStaff


class HasStoreProfile(BasePermission):
    message = _('You need to complete your profile to perform this action.')

    def has_permission(self, request, view):
        return super().has_permission(request, view) \
               and IsAuthenticated().has_permission(request, view) \
               and IsNotStaff().has_permission(request, view) \
               and bool(getattr(request.user, 'profile', None))
