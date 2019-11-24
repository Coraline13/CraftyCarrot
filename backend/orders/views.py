from collections import defaultdict

from django.db import transaction
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from orders.models import CartItem, Order, OrderItem
from orders.serializers import CartItemSerializer, CartItemUpdateSerializer, OrderSerializer
from store.permissions import HasStoreProfile


class CartViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = CartItem.objects.none()
    permission_classes = [HasStoreProfile]
    lookup_field = 'product'

    def get_queryset(self):
        if self.request and self.request.user and self.request.user.is_authenticated:
            return CartItem.objects.filter(profile=self.request.user.profile)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            return CartItemSerializer
        return CartItemUpdateSerializer


class OrderCreateView(mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer
    permission_classes = [HasStoreProfile]

    @swagger_auto_schema(request_body=no_body, operation_id='placeOrder', responses={200: OrderSerializer(many=True)})
    def create(self, request, *args, **kwargs):
        """Places orders for all products currently in the cart."""
        me = self.request.user.profile
        with transaction.atomic():
            if not me.cart.count():
                raise NotFound('No items in cart.')

            products_by_seller = defaultdict(list)
            for item in me.cart.all():  # type: CartItem
                prod = item.product
                products_by_seller[prod.seller].append(dict(product=prod, quantity=item.quantity, unit=prod.unit,
                                                            subtotal=prod.unit_price * item.quantity))

            orders = []
            for seller, products in products_by_seller.items():
                order = Order.objects.create(buyer=me, seller=seller)
                for prod in products:
                    OrderItem.objects.create(order=order, **prod)
                orders.append(order)

            me.cart.all().delete()
            serializer = self.get_serializer(many=True, instance=orders)
            return Response(serializer.data, status=201)


class OrderListView(mixins.ListModelMixin, GenericViewSet):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer
    permission_classes = [HasStoreProfile]

    def get_queryset(self):
        if self.request and self.request.user and self.request.user.is_authenticated:
            me = self.request.user.profile
            return Order.objects.filter(Q(buyer=me) | Q(seller=me))
        return super().get_queryset()
