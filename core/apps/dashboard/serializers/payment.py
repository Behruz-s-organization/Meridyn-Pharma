# rest framework
from rest_framework import serializers

# orders
from core.apps.orders.models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField(method_name='get_employee_name')
    factory = serializers.SerializerMethodField(method_name='get_factory')

    class Meta:
        model = Payment
        fields = [
            'id', 'employee_name', 'factory', 'price', 'created_at'
        ]

    def get_employee_name(self, obj):
        return obj.order.employee_name

    def get_factory(self, obj):
        return {
            'id': obj.order.factory.id,
            'name': obj.order.factory.name,
        }
