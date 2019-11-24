from django.urls import path
from rest_framework.routers import SimpleRouter

from orders.views import CartViewSet, OrderCreateView, OrderListView

router = SimpleRouter()
router.register('cart', CartViewSet)
router.register('place', OrderCreateView)
router.register('history', OrderListView)

urlpatterns = router.urls +[
]
