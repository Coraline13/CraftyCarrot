from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework_recursive.fields import RecursiveField

from main.serializers import FlatNestedSerializerMixin
from store.models import StoreProfile, Product, Category
from users.serializers import UserSerializer


class ProductNestedSerializer(ModelSerializer):
    category = serializers.SlugRelatedField('slug', queryset=Category.objects.all())
    category_name = serializers.ReadOnlyField(source='category.name')

    def create(self, validated_data):
        user = self.context['request'].user
        related_objects = {'seller': user.profile}
        validated_data.update(related_objects)
        return super().create(validated_data)

    class Meta:
        model = Product
        fields = ('category', 'category_name', 'seller', 'title', 'unit', 'unit_price', 'quantity')
        read_only_fields = ('seller',)
        ref_name = None


class StoreProfileSerializer(FlatNestedSerializerMixin, ModelSerializer):
    user = UserSerializer()
    products = ProductNestedSerializer(many=True)
    is_self = serializers.SerializerMethodField()

    def get_is_self(self, profile) -> bool:
        """Shows if this profile is the profile of the user authenticated with the current request."""
        request = self.context.get('request')
        me = getattr(getattr(request, 'user', None), 'profile', None)
        return profile == me

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user

        if user and user.is_authenticated:
            if hasattr(user, 'profile') and user.profile:
                raise serializers.ValidationError('user already has a StoreProfile!')

        related_objects = {'user': user}
        self._update_flattened_field(validated_data, related_objects=related_objects)
        validated_data.update(related_objects)
        return super().create(validated_data)

    class Meta:
        model = StoreProfile
        user_fields = ('email', 'first_name', 'last_name')
        fields = user_fields + ('is_self', 'phone', 'city', 'address', 'person_type', 'seller_type', 'products')
        read_only_fields = ('email',)
        flatten_fields = {'user': user_fields}
        extra_kwargs = {k: {'required': False} for k in fields}


class StoreProfileCreateSerializer(StoreProfileSerializer):
    class Meta(StoreProfileSerializer.Meta):
        fields = tuple(f for f in StoreProfileSerializer.Meta.fields if f != 'products')
        extra_kwargs = {k: {'required': True} for k in StoreProfileSerializer.Meta.fields
                        if k not in StoreProfileSerializer.Meta.read_only_fields}


class StoreProfileNestedSerializer(StoreProfileSerializer):
    class Meta(StoreProfileSerializer.Meta):
        fields = tuple(f for f in StoreProfileSerializer.Meta.fields if f != 'products')
        ref_name = None


class ProductListSerializer(ProductNestedSerializer):
    seller = StoreProfileNestedSerializer(read_only=True)


class ProductDetailSerializer(ProductListSerializer):
    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ('description',)


class CategorySerializer(ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'children')


class CategoryFlatSerializer(ModelSerializer):
    parent = SlugRelatedField('slug', read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'parent')
