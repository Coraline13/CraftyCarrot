"""
Django settings for contest project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os

from django.utils.crypto import get_random_string
from django.utils.encoding import force_text
from django.utils.text import slugify
from django.utils.translation import gettext_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BASE_DIR)


def getenv_assert(key):
    result = os.getenv(key, None)
    assert result, f'the {key} environment variable must be set'
    return result


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'users',
    'store',
    'orders',

    'adminsortable',
    'rangefilter',
    'phonenumber_field',
    'django_filters',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'import_export',
    'django_extensions',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.stackexchange',
    'allauth.socialaccount.providers.github',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'users.middleware.TokenSessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'locmem-default',
    },
    'session': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'locmem-session',
    },
    'swagger': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'locmem-session',
    },
}

MEMCACHED_URL = os.getenv('MEMCACHED_URL', None)

if MEMCACHED_URL:
    memcached_cache = {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': MEMCACHED_URL,
        'KEY_PREFIX': slugify(os.getenv('EXTERNAL_URL', get_random_string()))[:30],
    }
    CACHES['default'] = dict(memcached_cache)
    CACHES['session'] = dict(memcached_cache)

LOGS_DIR = os.path.join(REPO_ROOT, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'pipe_separated': {
            'format': '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        }
    },
    'handlers': {
        'debug_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'debug.log'),
            'formatter': 'pipe_separated',
            'encoding': 'utf-8',
        },
        'sql_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'sql.log'),
            'formatter': 'pipe_separated',
            'encoding': 'utf-8',
        },
        'console_log': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'pipe_separated',
        }
    },
    'loggers': {
        '': {
            'handlers': ['debug_log', 'console_log'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['debug_log', 'console_log'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['debug_log', 'console_log'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['sql_log'],
            'propagate': False,
        },
    },
}

WSGI_APPLICATION = 'main.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    # regular django auth for admin panel
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    # login via API token
    'users.backends.TokenBackend',
]

# django.contrib.sites is required by allauth
SITE_ID = 1
ACCOUNT_ADAPTER = 'users.auth.AccountAdapter'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_DISPLAY = force_text
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
# disabling HMAC for e-mail confirmation tokens (switching to db state) is necessary for the cooldown to work
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 4
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
SET_PASSWORD_ON_EMAIL_CONFIRMATION = False

API_PREFIX = '/api/'
PHONENUMBER_DEFAULT_REGION = 'RO'

CKEDITOR_UPLOAD_PATH = "admin/uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
    'basic': {
        'toolbar': 'basic',
        'height': 200,
        'toolbar_basic': [
            {'name': 'document', 'items': ['Source', '-']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
        ]
    },
}

FILE_UPLOAD_PERMISSIONS = 0o640

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

USE_I18N = True
USE_L10N = True

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', gettext_lazy('English')),
)

USE_TZ = True
TIME_ZONE = 'Europe/Bucharest'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(REPO_ROOT, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(REPO_ROOT, 'media')
os.makedirs(MEDIA_ROOT, exist_ok=True)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.backends.TokenAuthentication',
    ),
    'EXCEPTION_HANDLER': 'main.api.exceptions.validation_error_handler',
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'VALIDATOR_URL': None,

    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': False,
    'REFETCH_SCHEMA_ON_LOGOUT': False,

    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },

    'SPEC_URL': ('swagger-text', {'format': '.yaml'}),
    'DEFAULT_INFO': 'main.api.info',
    'DEFAULT_AUTO_SCHEMA_CLASS': 'main.api.openapi.XtecSwaggerAutoSchema',
    'DEFAULT_GENERATOR_CLASS': 'main.api.openapi.XtecSwaggerSchemaGenerator',
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
