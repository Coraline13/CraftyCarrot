from collections import Mapping, OrderedDict, Sequence

from django.core.exceptions import NON_FIELD_ERRORS as DJANGO_NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler


def validation_error_handler(exc, context):
    if isinstance(exc, serializers.ValidationError):
        if not isinstance(exc.detail, Mapping):
            detail = exc.detail if isinstance(exc.detail, Sequence) else [exc.detail]
            exc = serializers.ValidationError({api_settings.NON_FIELD_ERRORS_KEY: detail})
    elif isinstance(exc, ValidationError):
        default_code = getattr(exc, 'code', None) or 'invalid'
        try:
            error_dict = exc.error_dict
            if DJANGO_NON_FIELD_ERRORS in error_dict:
                error_dict[api_settings.NON_FIELD_ERRORS_KEY] = error_dict.pop(DJANGO_NON_FIELD_ERRORS)
        except AttributeError:
            error_dict = {api_settings.NON_FIELD_ERRORS_KEY: exc.error_list}

        error_dict = OrderedDict([
            (key, [serializers.ErrorDetail(e.message % (e.params or ()),
                                           e.code if e.code else default_code)
                   for e in error_list])
            for key, error_list in error_dict.items()])
        exc = serializers.ValidationError(error_dict, default_code)

    return exception_handler(exc, context)
