from django.contrib import admin

# orders
from core.apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee_name', 'advance', 'paid_price', 'total_price']
    inlines = [OrderItemInline]