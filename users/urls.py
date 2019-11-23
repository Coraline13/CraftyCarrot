from django.urls import include, path

urlpatterns = [
    path('', include('users.auth.urls')),
]
