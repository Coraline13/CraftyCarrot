from urllib.parse import urlparse

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.shortcuts import resolve_url

from ..models import User


class AdminPasswordResetForm(auth_forms.PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        self.get_users(email)
        return email

    def get_users(self, email):
        try:
            user = User._default_manager.filter(**{
                '%s__iexact' % User.get_email_field_name(): email,
            }).get()
        except MultipleObjectsReturned:
            raise ValidationError('There is more than one user associated with that e-mail address.', code='invalid')
        except User.DoesNotExist:
            raise ValidationError('No user was found matching that e-mail address.', code='invalid')

        if not user.is_active:
            raise ValidationError('The specified user is blocked.', code='invalid')
        if not user.is_staff:
            raise ValidationError('The specified user is not a staff member.', code='invalid')

        return [user]

    def save(self, **kwargs):
        request = kwargs.get('request', None)
        if request:
            url = urlparse(request.build_absolute_uri())
            if url.scheme and url.hostname:
                origin = f'{url.hostname}:{url.port}' if url.port else url.hostname
                kwargs['domain_override'] = origin
                kwargs['use_https'] = url.scheme == 'https'
        super().save(**kwargs)


class AdminPasswordResetView(auth_views.PasswordResetView):
    form_class = AdminPasswordResetForm

    def form_valid(self, form):
        return super().form_valid(form)


class AdminPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url('admin:login')
        return context
