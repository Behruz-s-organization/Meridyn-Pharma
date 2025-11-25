from django.contrib import admin

# shared
from core.apps.shared.models import Location, UserLocation



@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'longitude', 'latitude', 'created_at']


@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'longitude', 'latitude']