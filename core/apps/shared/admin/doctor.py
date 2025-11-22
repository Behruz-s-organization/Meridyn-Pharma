from django.contrib import admin

# shared
from core.apps.shared.models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_number']
    search_fields = list_display

