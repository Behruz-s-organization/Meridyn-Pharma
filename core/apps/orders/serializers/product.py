from rest_framework import serializers

# orders
from core.apps.orders.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'created_at'
        ]