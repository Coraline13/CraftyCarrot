from admin_numeric_filter.admin import RangeNumericFilter
from adminsortable.admin import SortableAdmin
from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from related_admin import RelatedFieldAdmin

from main.admin import admin_link_field
from store.models import StoreProfile, Product, Category


@admin.register(StoreProfile)
class StoreProfileAdmin(RelatedFieldAdmin):
    list_filter = ('person_type', 'seller_type')
    list_display = ('__str__', 'user__username', 'user__email', 'phone',
                    'person_type', 'seller_type', 'city', 'address')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller_link', 'category_link', 'unit', 'unit_price', 'quantity', 'created')
    list_filter = (('created', DateRangeFilter), 'category', ('quantity', RangeNumericFilter))
    ordering = ('-created',)
    date_hierarchy = 'created'

    seller_link = admin_link_field(Product, 'seller')
    category_link = admin_link_field(Product, 'category')


@admin.register(Category)
class CategoryAdmin(SortableAdmin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
