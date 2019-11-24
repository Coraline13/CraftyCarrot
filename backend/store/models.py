from adminsortable.models import SortableMixin
from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from main.models import CreatedModifiedMixin

person_type_choices = [
    ('private', 'Private'),
    ('company', 'Company'),
]


class StoreProfile(CreatedModifiedMixin, models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = PhoneNumberField()
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=512)
    person_type = models.CharField(max_length=32, choices=person_type_choices, blank=True)
    seller_type = models.CharField(max_length=32, choices=person_type_choices, blank=True)

    def __str__(self):
        return str(self.user)


class Category(SortableMixin, models.Model):
    class Meta:
        ordering = ['order_index']
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)
    order_index = models.IntegerField(default=0, editable=False, db_index=True)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'{self.name} ({self.slug})'


class Product(CreatedModifiedMixin, models.Model):
    seller = models.ForeignKey('StoreProfile', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4096)
    unit = models.CharField(max_length=10)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField()

    @property
    def owner(self):
        return self.seller

    def __str__(self):
        return f'{self.title}'
