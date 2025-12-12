from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# accounts
from core.apps.accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ['telegram_id', 'first_name', 'last_name', 'is_active']
    search_fields = ['telegram_id', 'first_name', 'last_name']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "region", "telegram_id"),
            },
        ),
    )

admin.site.unregister(Group)