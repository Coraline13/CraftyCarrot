from django.urls import path

from store.views import OwnStoreProfileView

urlpatterns = [
    path('profile/', OwnStoreProfileView.as_view()),
]
