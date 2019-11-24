from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from main.admin import admin_link_field, MultipleChoiceFieldListFilter
from orders.models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'buyer_link', 'seller_link', 'created', 'status')
    list_filter = ('status', ('created', DateRangeFilter), ('buyer', MultipleChoiceFieldListFilter),
                   ('seller', MultipleChoiceFieldListFilter))
    ordering = ('-created',)
    date_hierarchy = 'created'

    buyer_link = admin_link_field(Order, 'buyer')
    seller_link = admin_link_field(Order, 'seller')
