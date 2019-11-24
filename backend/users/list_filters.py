from django.contrib import admin
from django.db.models import F


class HasProfileListFilter(admin.SimpleListFilter):
    title = 'profile status'
    parameter_name = 'has_profile'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Has profile'),
            ('false', 'No profile'),
        )

    def queryset(self, request, queryset):
        if self.value() not in ('true', 'false'):
            return queryset

        return queryset.filter(profile__isnull=not self.value() == 'true')


class HasVerifiedEmailListFilter(admin.SimpleListFilter):
    title = 'e-mail verification status'
    parameter_name = 'has_verified_email'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Verified'),
            ('false', 'Not verified'),
        )

    def queryset(self, request, queryset):
        if self.value() not in ('true', 'false'):
            return queryset

        if self.value() == 'true':
            return queryset.filter(emailaddress__email=F('email'), emailaddress__verified=True)
        else:
            return queryset.exclude(emailaddress__email=F('email'), emailaddress__verified=True)
