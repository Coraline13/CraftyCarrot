from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from main.models import CreatedModifiedMixin
from store.models import StoreProfile, Product


order_status_choices = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('delivery', 'Delivery'),
    ('finished', 'Finished'),
]


class Order(CreatedModifiedMixin, models.Model):
    buyer = models.ForeignKey(StoreProfile, on_delete=models.PROTECT, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    status = models.CharField(max_length=30, choices=order_status_choices)

    def __str__(self):
        return f'Order #{self.id} by {self.buyer} at {self.created}'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='+')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit = models.CharField(max_length=10)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f'{self.product}, {self.quantity} {self.unit} @ {self.total_price}'

    class Meta:
        unique_together = ('order', 'product')


class CartItem(models.Model):
    profile = models.ForeignKey(StoreProfile, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('profile', 'product')
