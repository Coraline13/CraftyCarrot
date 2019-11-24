from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from orders.models import CartItem
from store.models import Product
from store.serializers import ProductNestedSerializer, SetOwnProfileMixin


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
            defaults={'quantity': validated_data['quantity']})
        return cartitem

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')
        profile_field_name = 'profile'
