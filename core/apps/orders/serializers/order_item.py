# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# orders
from core.apps.orders.models import OrderItem



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'quantity', 'total_price'
        ]