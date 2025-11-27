from django.contrib import admin


# shared
from core.apps.shared.models import Factory



@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']