from rest_framework.routers import SimpleRouter

from orders.views import CartViewSet

router = SimpleRouter()
router.register('cart', CartViewSet)

urlpatterns = router.urls +[

]
