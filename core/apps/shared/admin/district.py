from django.contrib import admin

# shared
from core.apps.shared.models import District


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name']

    