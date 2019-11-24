from adminsortable.admin import SortableAdmin
from django.contrib import admin

from store.models import StoreProfile, Product, Category


@admin.register(StoreProfile)
class StoreProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(SortableAdmin, admin.ModelAdmin):
    pass
