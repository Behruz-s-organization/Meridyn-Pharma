from django.contrib import admin
from django.contrib.auth.models import Group

# accounts
from core.apps.accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'first_name', 'last_name', 'is_active']
    search_fields = ['telegram_id', 'first_name', 'last_name']


admin.site.unregister(Group)