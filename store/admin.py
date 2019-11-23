from django.contrib import admin

from store.models import StoreProfile


@admin.register(StoreProfile)
class StoreProfileAdmin(admin.ModelAdmin):
    pass
