# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# orders
from core.apps.orders.models import OrderItem, Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'quantity', 'total_price'
        ]



class OrderUpdateItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=15, decimal_places=2)

    def validate(self, attrs):
        product = Product.objects.filter(id=attrs['product_id']).first()
        if not product:
            raise serializers.ValidationError({"product": "Product not found"})
        attrs['product'] = product
        return attrs

