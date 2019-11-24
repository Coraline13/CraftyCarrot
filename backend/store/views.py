from django.db.models import Q
from django_filters import FilterSet, filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from str2bool import str2bool

from store.models import StoreProfile, Product, Category
from store.permissions import HasStoreProfile, IsOwnerOrReadOnly
from store.serializers import StoreProfileSerializer, StoreProfileCreateSerializer, ProductListSerializer, \
    ProductDetailSerializer, CategorySerializer, CategoryFlatSerializer


class OwnStoreProfileView(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    serializer_class = StoreProfileSerializer
    queryset = StoreProfile.objects.none()
    swagger_child_tags = ['profile']

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


class ProductFilterSet(FilterSet):
    city = filters.AllValuesMultipleFilter('seller__city')
    min_price = filters.NumberFilter(field_name="unit_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="unit_price", lookup_expr='lte')

    category = filters.AllValuesMultipleFilter(field_name="category__slug", method='filter_category')

    def filter_category(self, queryset, name, categories):
        return queryset.filter(category__slug__in=categories)

    sort = filters.OrderingFilter(fields=['created', 'quantity', 'unit_price'])

    class Meta:
        model = Product
        fields = ['category', 'city', 'min_price', 'max_price']


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    swagger_child_tags = ['products']
    filterset_class = ProductFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request and self.request.user and self.request.user.is_authenticated:
            me = self.request.user.profile
            qs = qs.filter(Q(seller__seller_type=me.person_type) | Q(seller=me))
        return qs

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update', 'partial_update'):
            return ProductDetailSerializer
        if self.action == 'list':
            return ProductListSerializer
        raise NotImplementedError(f"unknown action {self.action}")

    def is_read_only(self):
        return self.action in ('list', 'retrieve')

    def get_permissions(self):
        if self.is_read_only():
            return []
        return super().get_permissions()


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(in_=openapi.IN_QUERY, name='flat', type=openapi.TYPE_BOOLEAN, required=False, default=True)
    ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False) or str2bool(self.request.query_params.get('flat', 'true')):
            return CategoryFlatSerializer
        return CategorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if not str2bool(self.request.query_params.get('flat', 'true')):
            qs = qs.filter(parent__isnull=True)
        return qs
