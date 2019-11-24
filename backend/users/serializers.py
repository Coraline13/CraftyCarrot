from allauth.account import app_settings as allauth_settings
from django.contrib.auth.password_validation import MinimumLengthValidator, get_default_password_validators
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Token, User


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'created', 'expiration',)
        read_only_fields = fields


def password_min_length():
    validators = get_default_password_validators()
    for validator in validators:
        if isinstance(validator, MinimumLengthValidator):
            return validator.min_length

    return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('username', 'email')
        extra_kwargs = {
            'username': {
                'min_length': allauth_settings.USERNAME_MIN_LENGTH,
            },
            'email': {
                'max_length': allauth_settings.EMAIL_MAX_LENGTH,
                'validators': [RegexValidator(r'^\S*$')],
            },
            'password': {
                'min_length': password_min_length(),
                'write_only': True,
            },
        }
