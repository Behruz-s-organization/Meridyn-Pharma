# django 
from django.db import transaction

# rest framework
from rest_framework import serializers

# orders 
from core.apps.orders.models import Order, OrderItem
from core.apps.orders.serializers.order_item import OrderItemSerializer
# shared
from core.apps.shared.models import Pharmacy


class OrderCreateSerializer(serializers.Serializer):
    pharmacy_id = serializers.IntegerField()
    paid_price = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=15, decimal_places=2)
    advance = serializers.FloatField()
    employee_name = serializers.CharField()
    items = OrderItemSerializer(many=True)

    def validate(self, data):
        pharmacy = Pharmacy.objects.filter(id=data['pharmacy_id']).first()
        if not pharmacy:
            raise serializers.ValidationError({"pharmancy_id": "Pharmancy not found"})
        data['pharmacy'] = pharmacy
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            order = Order.objects.create(
                pharmacy=validated_data.get('pharmacy'),
                paid_price=validated_data.get('paid_price'),
                advance=validated_data.get('advance'),
                employee_name=validated_data.get('employee_name'),
                total_price=validated_data.get('total_price'),
            )
            order_items = []
            for order_item in validated_data.get('items'):
                order_items(OrderItem(
                    product=order_item.get('product'),
                    order=order,
                    quantity=order_item.get('quantity'),
                    total_price=order_item.get('total_price'),
                ))
            OrderItem.objects.bulk_create(order_items)
            return order
        
    
class OrderListSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'pharmacy', 'total_price', 'paid_price', 'advance', 'employee_name',
            'order_items'
        ]