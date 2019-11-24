from urllib.parse import urlparse

import dj_database_url
import dj_email_url
from str2bool import str2bool

from .base import *  # noqa: F403

DEBUG = str2bool(os.getenv('DJANGO_DEBUG', False))

EXTERNAL_URL = getenv_assert('EXTERNAL_URL')
ALLOWED_HOSTS = ['*']

USE_X_FORWARDED_PORT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv_assert('DJANGO_SECRET_KEY')

SESSION_COOKIE_SECURE = urlparse(EXTERNAL_URL).scheme == 'https'
CSRF_COOKIE_SECURE = urlparse(EXTERNAL_URL).scheme == 'https'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = urlparse(EXTERNAL_URL).scheme

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')

PRIVATE_STORAGE_INTERNAL_URL = '/private-files/'
PRIVATE_STORAGE_NGINX_VERSION = '1.12.2'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # db config from DATABASE_URL env variable; e.g.:
    # mysql://itec:PASWORD@prometheus.shiva.ligaac.ro:3306/itec_dev_2018
    # sqlite:///tmp/db.sqlite3
    'default': dj_database_url.config(conn_max_age=600)
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'

for engine in TEMPLATES:
    if 'loaders' in engine and not engine.get('debug', DEBUG):
        engine['loaders'] = [('django.template.loaders.cached.Loader', engine['loaders'])]

# e-mail config from EMAIL_URL env variable; e.g.:
# console:// - print to stdout
# smtp://mailhog.ligaac.ro:1025 - unencrypted and unauthenticated smtp
# smtp:// - send via local MTA (sendmail, postfix, etc)
# submit://sendgrid_username:sendgrid_password@smtp.sendgrid.com - port 587 with STARTTLS
# smtp://user@domain.com:pass@smtp.example.com:465/?ssl=True - port 465 with SSL
vars().update(dj_email_url.config())
DEFAULT_FROM_EMAIL = getenv_assert('EMAIL_FROM')
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', "")

SILENCED_SYSTEM_CHECKS = [
    'security.W004',  # SECURE_HSTS_SECONDS
    'security.W008',  # SECURE_SSL_REDIRECT
]
