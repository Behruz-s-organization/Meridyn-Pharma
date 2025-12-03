# django
from django.contrib import admin

# shared
from core.apps.shared.models import Support


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ['id', 'problem', 'date', 'user']
    search_fields = ['problem', 'user__first_name', 'user__last_name']
    