from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.urls import reverse
from django.utils.functional import lazy


def update_qs(url: str, query_args: dict) -> str:
    scheme, netloc, path, query, fragment = urlsplit(url)
    pqs = parse_qs(query)
    pqs.update(query_args)
    query = urlencode(pqs, doseq=True)
    return urlunsplit((scheme, netloc, path, query, fragment))


def reverse_with_query(viewname, urlconf=None, args=None, kwargs=None, current_app=None, query_args=None):
    url = reverse(viewname, urlconf, args, kwargs, current_app)
    if query_args:
        url = update_qs(url, query_args)

    return url


reverse_with_query_lazy = lazy(reverse_with_query, str)


def admin_reregister(*models, site=None):
    def wrapper(admin_class):
        admin_site = site or admin.site
        try:
            admin_site.unregister(*models)
        except NotRegistered:
            pass
        return admin.register(*models, site=site)(admin_class)

    return wrapper
