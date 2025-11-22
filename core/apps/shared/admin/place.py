from django.contrib import admin

# shared
from core.apps.shared.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'district']
    search_fields = ['name']