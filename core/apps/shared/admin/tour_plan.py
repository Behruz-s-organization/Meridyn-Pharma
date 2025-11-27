from django.contrib import admin

# shared
from core.apps.shared.models import TourPlan


@admin.register(TourPlan)
class TourPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'place_name', 'longitude', 'latitude', 'user']
    