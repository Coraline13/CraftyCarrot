from urllib.parse import unquote

from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin, messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import GroupAdmin, UserAdmin, sensitive_post_parameters_m
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import ModelForm, ModelMultipleChoiceField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter

from main.util import reverse_with_query, admin_reregister
from .auth import form_valid_or_raise
from .auth.admin import AdminPasswordResetForm, AdminPasswordResetView
from .list_filters import HasProfileListFilter, HasVerifiedEmailListFilter
from .models import User


# class ContestantProfileInlineAdmin(StackedInline):
#     model = ContestantProfile
#     extra = 0
#     can_delete = False
#
#     def has_delete_permission(self, *args, **kwargs):
#         return False


class AdminUserCreationForm(UserCreationForm):
    """
    A UserCreationForm with optional password inputs.
    """
    password1 = None
    password2 = None

    def save(self, commit=True):
        return ModelForm.save(self, commit)


@admin.register(User)
class UserAdminWithProfile(UserAdmin):
    # inlines = (ContestantProfileInlineAdmin,)
    list_display = ('username', 'emailaddress_link', 'has_verified_email',
                    'first_name', 'last_name', 'is_staff', 'date_joined')
    # list_display += ('profile_link',)
    # list_select_related = ('profile',)

    list_filter = UserAdmin.list_filter
    list_filter += (('date_joined', DateRangeFilter), HasProfileListFilter, HasVerifiedEmailListFilter)
    date_hierarchy = 'date_joined'
    ordering = ('-date_joined',)

    add_form = AdminUserCreationForm
    add_fieldsets = UserAdmin.add_fieldsets
    add_fieldsets[0][1]['fields'] = ('username', 'email', 'first_name', 'last_name',
                                     'is_staff', 'is_superuser', 'groups', 'user_permissions')

    def get_inline_instances(self, request, obj=None):
        return obj and super().get_inline_instances(request, obj) or []

    def save_model(self, request, user, form, change):
        if not change:
            user.set_unusable_password()

        super(UserAdmin, self).save_model(request, user, form, change)

        if not change and user.is_staff:
            reset_form = AdminPasswordResetForm({'email': user.email})
            reset_view = AdminPasswordResetView(request=request)

            form_valid_or_raise(reset_form)
            reset_view.form_valid(reset_form)
            messages.add_message(request, messages.INFO, 'An e-mail has been sent to %(email)s with instructions '
                                                         'for choosing a password.' % {'email': user.email})

    def check_ldap_user(self, obj):
        return obj.has_ldap_user()

    check_ldap_user.boolean = True
    check_ldap_user.short_description = 'from LDAP'
    check_ldap_user.admin_order_field = 'is_from_ldap'

    def emailaddress_link(self, obj):
        email = obj.email
        if not email:
            return None

        try:
            emailaddress = next(ea for ea in obj.emailaddress_set.all() if ea.email == email)
            link = reverse("admin:account_emailaddress_change", args=(emailaddress.id,))
            return mark_safe('<a href="%s">%s</a>' % (link, escape(email)))
        except StopIteration:
            add_form_args = {'user': obj.id, 'email': email, 'primary': 1}
            link = reverse_with_query("admin:account_emailaddress_add", query_args=add_form_args)
            style = {
                "background-position": "right 0px center",
                "padding-left": "0px",
                "padding-right": "16px",
            }
            style = "; ".join(f'{attr}: {val}' for attr, val in style.items())
            return mark_safe('<a href="%s" class="addlink" style="%s">%s</a>' % (link, style, escape(email)))

    emailaddress_link.short_description = 'E-mail'
    emailaddress_link.admin_order_field = 'email'

    # def profile_link(self, obj):
    #     profile = getattr(obj, 'profile', None)
    #     if not profile:
    #         return ''
    #
    #     profile_link = reverse(f"admin:{get_xtec_app_label()}_contestantprofile_change", args=(profile.id,))
    #     return mark_safe('<a href="%s">%s</a>' % (profile_link, escape(profile.id)))
    #
    # profile_link.allow_tags = True
    # profile_link.short_description = 'Contestant profile'
    # profile_link.admin_order_field = 'user__profile__isnull'

    def has_verified_email(self, obj):
        return any(ea.verified for ea in obj.emailaddress_set.all() if ea.email == obj.email)

    has_verified_email.boolean = True
    has_verified_email.short_description = 'E-mail verified'
    has_verified_email.admin_order_field = 'emailaddress__verified'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('emailaddress_set')
        return qs

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        user = self.get_object(request, unquote(id))
        if user.has_ldap_user(request):
            messages.error(request, 'Cannot set Django password for LDAP user. Contact the administrator.')
            return HttpResponseRedirect(
                reverse(
                    '%s:%s_%s_change' % (
                        self.admin_site.name,
                        user._meta.app_label,
                        user._meta.model_name,
                    ),
                    args=(user.pk,),
                )
            )
        return super().user_change_password(request, id, form_url)


class GroupAdminForm(ModelForm):
    """
    ModelForm that adds an additional multiple select field for managing
    the users in the group.
    """
    members = ModelMultipleChoiceField(
        User.objects.filter(is_staff=True, is_superuser=False),
        widget=FilteredSelectMultiple('Users', False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            initial_users = self.instance.user_set.values_list('pk', flat=True)
            self.initial['members'] = initial_users

    def save(self, *args, **kwargs):
        kwargs['commit'] = True
        return super(GroupAdminForm, self).save(*args, **kwargs)

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['members'])


@admin_reregister(Group)
class GroupMembersAdmin(GroupAdmin):
    """
    Customized GroupAdmin class that uses the customized form to allow management of users within a group.
    """
    form = GroupAdminForm


@admin_reregister(EmailAddress)
class EmailAddressDetailAdmin(EmailAddressAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('admin:index')


# noinspection PyUnresolvedReferences
def unregister_admin_junk():
    # import admin modules to trigger model registration
    import django.contrib.sites.admin
    import django.contrib.auth.admin
    import allauth.account.admin
    import allauth.socialaccount.admin

    # unregister unwanted models
    from django.contrib.sites.models import Site
    from django.contrib.auth.models import Group
    from allauth.account.models import EmailConfirmation
    from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

    admin.site.unregister(Site)
    admin.site.unregister(SocialAccount)
    admin.site.unregister(SocialApp)
    admin.site.unregister(SocialToken)
    admin.site.unregister(EmailConfirmation)


unregister_admin_junk()
