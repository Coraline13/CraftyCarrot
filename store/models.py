from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


person_type_choices = [
    ('private', 'Private'),
    ('company', 'Company'),
]


class StoreProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = PhoneNumberField()
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=512)
    person_type = models.CharField(max_length=32, choices=person_type_choices, blank=True)
    seller_type = models.CharField(max_length=32, choices=person_type_choices, blank=True)

    def __str__(self):
        return str(self.user)
