import dj_database_url
import dj_email_url

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
EXTERNAL_URL = 'http://localhost'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"


def get_local_ips():
    import ifaddr

    for adapter in ifaddr.get_adapters():
        for ip in adapter.ips:
            if isinstance(ip.ip, str):
                yield ip.ip


ALLOWED_HOSTS.extend(get_local_ips())

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# See production.py for DATABASE_URL and EMAIL_URL format

db_path = os.path.join(REPO_ROOT, f'db.sqlite3')
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///' + db_path)
}

vars().update(dj_email_url.config(default='console://'))
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

PRIVATE_STORAGE_SERVER = 'django'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z5b*=z^@^3e)3_y$f*s-0tt13jwczdjk*0aj$qefnt_b&u!)ee'
