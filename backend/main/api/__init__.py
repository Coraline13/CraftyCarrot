from django.conf import settings
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from phonenumber_field.modelfields import PhoneNumberField as PhoneNumberModelField
from phonenumber_field.serializerfields import PhoneNumberField as PhoneNumberSerializerField
from rest_framework import permissions, serializers
from rest_framework.documentation import include_docs_urls
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.routers import SimpleRouter

try:
    del UpdateAPIView.put
    del RetrieveUpdateAPIView.put
    del RetrieveUpdateDestroyAPIView.put
    SimpleRouter.routes[2].mapping.pop('put', None)
except AttributeError:
    pass

serializers.ModelSerializer.serializer_field_mapping[PhoneNumberModelField] = PhoneNumberSerializerField

info = openapi.Info(
    title="iTEC 2019 Web Store API",
    default_version="v1",
    description="""
[Hatz](https://www.youtube.com/watch?v=xJoHxKLJqNI)

[Admin panel](/admin/)
[DRF Docs](/api/docs/)
[ReDoc](/api/redoc/)
""",
)

swagger_view = get_schema_view(
    info,
    validators=[],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def is_api_request(request):
    return request.path.startswith(settings.API_PREFIX)


swagger_spec_view = swagger_view.without_ui(cache_timeout=None, cache_kwargs={'cache': 'swagger'})
swagger_ui_view = swagger_view.with_ui('swagger', cache_timeout=None, cache_kwargs={'cache': 'swagger'})
redoc_view = swagger_view.with_ui('redoc', cache_timeout=None, cache_kwargs={'cache': 'swagger'})

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', swagger_spec_view, name='swagger-text'),
    path('swagger/', swagger_ui_view, name='swagger-ui'),
    path('redoc/', redoc_view),
    path('docs/', include_docs_urls(title=info.title, description=info.description)),
    path('', RedirectView.as_view(pattern_name='swagger-ui', permanent=True)),

    path('user/', include('users.urls')),
    path('store/', include('store.urls')),
    path('orders/', include('orders.urls')),
]
