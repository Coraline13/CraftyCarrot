import binascii
import os
import time
from collections import Mapping
from datetime import timedelta

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import AbstractUser
from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.template.defaultfilters import title
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.utils import encoders, json


def validate_json(value):
    try:
        if value:
            assert isinstance(json.loads(json.dumps(value, cls=encoders.JSONEncoder)), Mapping)
    except Exception:
        raise ValidationError(_('Not a valid JSON object: %(value)s'), params={'value': value})


class JSONField(models.TextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validate_json)
        self.default = kwargs.pop('default', None) or {}

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, Mapping):
            return value

        s = super().to_python(value)
        if not s:
            return {}

        return json.loads(s) or {}

    def get_prep_value(self, value):
        if not value:
            return None

        return json.dumps(value, cls=encoders.JSONEncoder)

    def value_to_string(self, obj):
        return json.dumps(self.value_from_object(obj), cls=encoders.JSONEncoder)


class User(AbstractUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions and is identified by e-mail address.

    Email and password are required. Other fields are optional.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _("A user with that e-mail address already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    extra_confirmation_data = JSONField(blank=True, null=True, editable=False)

    def get_full_name(self):
        return title(super().get_full_name())

    def __str__(self):
        if self.first_name or self.last_name:
            return self.get_full_name()
        elif self.username:
            return self.username
        else:
            return self.id or '<empty User object>'


class TokenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user')


class Token(models.Model):
    """
    An access token that is associated with a user. This is essentially the
    same as the token model from Django REST Framework.
    """
    objects = TokenManager()

    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tokens")
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            self.expiration = timezone.now() + timedelta(days=7)
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

