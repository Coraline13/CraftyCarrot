from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from main.serializers import FlatNestedSerializerMixin
from store.models import StoreProfile
from users.serializers import UserSerializer


class StoreProfileSerializer(FlatNestedSerializerMixin, ModelSerializer):
    user = UserSerializer()

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
        fields = user_fields + ('phone', 'city', 'address', 'person_type', 'seller_type')
        read_only_fields = ('email',)
        flatten_fields = {'user': user_fields}
        extra_kwargs = {k: {'required': False} for k in fields}


class StoreProfileCreateSerializer(StoreProfileSerializer):
    class Meta(StoreProfileSerializer.Meta):
        extra_kwargs = {k: {'required': True} for k in StoreProfileSerializer.Meta.fields
                        if k not in StoreProfileSerializer.Meta.read_only_fields}
