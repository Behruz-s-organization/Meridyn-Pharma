from django.contrib import admin

# orders
from core.apps.orders.models import Product


admin.site.register(Product)