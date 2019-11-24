from adminsortable.admin import SortableAdmin
from django.contrib import admin
from related_admin import RelatedFieldAdmin

from store.models import StoreProfile, Product, Category


@admin.register(StoreProfile)
class StoreProfileAdmin(RelatedFieldAdmin):
    list_filter = ('person_type', 'seller_type')
    list_display = ('user__username', 'user__email', 'phone', 'person_type', 'seller_type', 'city', 'address')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(SortableAdmin, admin.ModelAdmin):
    pass
