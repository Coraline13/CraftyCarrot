from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from users.permissions import IsNotStaff


class HasStoreProfile(BasePermission):
    message = _('You need to complete your profile to perform this action.')

    def has_permission(self, request, view):
        return super().has_permission(request, view) \
               and IsAuthenticated().has_permission(request, view) \
               and IsNotStaff().has_permission(request, view) \
               and bool(getattr(request.user, 'profile', None))


class IsOwnerOrReadOnly(HasStoreProfile):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user.profile
