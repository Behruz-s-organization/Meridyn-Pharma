# django
from django.contrib import admin

# orders
from core.apps.orders.models import DistributedProduct


admin.site.register(DistributedProduct)