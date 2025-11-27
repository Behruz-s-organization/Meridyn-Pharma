# django 
from django.db import transaction
from django.core.files.base import ContentFile

# rest framework
from rest_framework import serializers

# orders 
from core.apps.orders.models import Order, OrderItem
from core.apps.orders.serializers.order_item import OrderItemSerializer
# shared
from core.apps.shared.models import Factory
# services
from core.services.generate_pdf import generate_order_pdf
from core.services.send_telegram_msg import send_to_telegram


class OrderCreateSerializer(serializers.Serializer):
    factory_id = serializers.IntegerField()
    paid_price = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=15, decimal_places=2)
    advance = serializers.FloatField()
    employee_name = serializers.CharField()
    items = OrderItemSerializer(many=True)

    def validate(self, data):
        factory = Factory.objects.filter(id=data['factory_id']).first()
        if not factory:
            raise serializers.ValidationError({"factory_id": "Factory not found"})
        data['factory'] = factory
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            user = self.context.get('user')
            order = Order.objects.create(
                factory=validated_data.get('factory'),
                paid_price=validated_data.get('paid_price'),
                advance=validated_data.get('advance'),
                employee_name=validated_data.get('employee_name'),
                total_price=validated_data.get('total_price'),
                user=user
            )
            order_items = []
            for order_item in validated_data.get('items'):
                order_items.append(OrderItem(
                    product=order_item.get('product'),
                    order=order,
                    quantity=order_item.get('quantity'),
                    total_price=order_item.get('total_price'),
                ))
            OrderItem.objects.bulk_create(order_items)

            # generate pdf file
            pdf_buffer = generate_order_pdf(order.id)

            file_name = f"order_{order.id}.pdf"
            order.file.save(file_name, ContentFile(pdf_buffer.getvalue()), save=False)

            order.save(update_fields=["file"]) 

            # send to telegram 
            
            send_to_telegram(user.telegram_id, order.id)
            return order
        
    
class OrderListSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    factory = serializers.SerializerMethodField(method_name='get_factory')

    class Meta:
        model = Order
        fields = [
            'id', 'factory', 'total_price', 'paid_price', 'advance', 'employee_name',
            'overdue_price', 'order_items', 'file'
        ]

    def get_factory(self, obj):
        return {
            'id': obj.factory.id,
            'name': obj.factory.name,
        }


class OrderUpdateSerializer(serializers.Serializer):
    paid_price = serializers.IntegerField()
    