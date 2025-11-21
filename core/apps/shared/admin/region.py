from django.contrib import admin

# shared
from core.apps.shared.models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'users_count']
    search_fields = ['name']