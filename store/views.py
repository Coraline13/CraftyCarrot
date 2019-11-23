from django.shortcuts import render
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from store.models import StoreProfile
from store.permissions import HasStoreProfile
from store.serializers import StoreProfileSerializer, StoreProfileCreateSerializer


class OwnStoreProfileView(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    serializer_class = StoreProfileSerializer
    queryset = StoreProfile.objects.none()

    def get_serializer_class(self):
        if self.method == 'post':
            return StoreProfileCreateSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset

        return StoreProfile.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.method in ('get', 'post'):
            return [IsAuthenticated()]
        return [HasStoreProfile()]

    @property
    def method(self):
        return self.request.method.lower()

    def get_object(self):
        return get_object_or_404(self.get_queryset())

    def get(self, request):
        return self.retrieve(request)

    def post(self, request):
        return self.create(request)

    def patch(self, request):
        return self.partial_update(request)

