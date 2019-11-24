from decimal import Decimal

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from orders.models import CartItem, Order, OrderItem
from store.models import Product
from store.serializers import ProductNestedSerializer, SetOwnProfileMixin, StoreProfileNestedSerializer


class CartItemSerializer(ModelSerializer):
    product = ProductNestedSerializer()

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')


class OtherUserProductRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        queryset = Product.objects.exclude(seller=self.context['request'].user.profile)
        return queryset


class CartItemUpdateSerializer(SetOwnProfileMixin, ModelSerializer):
    product = OtherUserProductRelatedField()

    def create(self, validated_data):
        cartitem, created = CartItem.objects.update_or_create(
            product=validated_data['product'],
            defaults={'quantity': validated_data['quantity'], **self.get_profile_kwargs()})
        return cartitem

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')
        profile_field_name = 'profile'


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.title')
    category = serializers.ReadOnlyField(source='product.category.name')

    class Meta:
        model = OrderItem
        fields = ('product', 'category', 'unit', 'quantity', 'subtotal')


class OrderSerializer(serializers.ModelSerializer):
    buyer = StoreProfileNestedSerializer()
    seller = StoreProfileNestedSerializer()
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order: Order):
        return sum([item.subtotal for item in order.items.all()], Decimal(0))

    class Meta:
        model = Order
        fields = ('buyer', 'seller', 'items', 'total_price')
        read_only_fields = fields
