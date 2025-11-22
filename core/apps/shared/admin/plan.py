from django.contrib import admin

# shared
from core.apps.shared.models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date']
    search_fields = list_display