# rest framework
from rest_framework import serializers

# orders
from core.apps.orders.models import DistributedProduct


class DistributedProductListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(method_name='get_product')
    user = serializers.SerializerMethodField(method_name='get_user')
    
    class Meta:
        model = DistributedProduct
        fields = [
            'id', 'product', 'quantity', 'employee_name', 'quantity', 'user', 'created_at', 'date'
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }
    
    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "price": obj.product.price,
        }
    