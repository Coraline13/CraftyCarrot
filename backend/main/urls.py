"""contest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from users.auth.admin import AdminPasswordResetCompleteView, AdminPasswordResetView


def dummy_view(request, *args, **kwargs):
    raise NotImplementedError("This view should be routed to client-side code.")


api_prefix = settings.API_PREFIX.lstrip('/')

client_urlpatterns = [
    # client-side route mappings for use with reverse()
    # these are used to build e-mail links and should be implemented client-side
    path('confirm-email/<str:key>', dummy_view, name='account_confirm_email'),
    path('{portal_prefix}reset-password/<str:uidb36>/<str:key>', dummy_view, name='account_reset_password_from_key'),
]

urlpatterns = [
    path('admin/reset/', AdminPasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/reset/sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/reset/done/', AdminPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),

    # utility redirects
    path('', RedirectView.as_view(url='/' + api_prefix)),
    path(f'{api_prefix}admin/', RedirectView.as_view(url='/admin')),

    # included only to appease allauth; not accesible in production
    path('accounts/', include('allauth.urls')),

    path('', include(client_urlpatterns)),
    path(api_prefix, include('main.api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
