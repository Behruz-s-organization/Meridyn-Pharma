from django.contrib import admin

# shared
from core.apps.shared.models import Pharmacy


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inn', 'owner_phone', 'responsible_phone']
    search_fields = list_display