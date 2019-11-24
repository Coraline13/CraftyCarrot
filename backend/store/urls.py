from django.urls import path
from rest_framework.routers import SimpleRouter

from store.views import OwnStoreProfileView, ProductViewSet, CategoryListView, CityListView

router = SimpleRouter()
router.register('products', ProductViewSet)

urlpatterns = router.urls + [
    path('profile/', OwnStoreProfileView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('cities/', CityListView.as_view()),
]
