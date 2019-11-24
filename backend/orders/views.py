from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from orders.models import CartItem
from orders.serializers import CartItemSerializer, CartItemUpdateSerializer
from store.permissions import HasStoreProfile


class CartViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = CartItem.objects.none()
    permission_classes = [HasStoreProfile]
    lookup_field = 'product'

    def get_queryset(self):
        return CartItem.objects.filter(profile=self.request.user.profile)

    def get_serializer_class(self):
        if self.action == 'list':
            return CartItemSerializer
        return CartItemUpdateSerializer
