# rest framework
from rest_framework import serializers

# orders
from core.apps.orders.models import DistributedProduct


class DistributedProductListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(method_name='get_product')
    
    class Meta:
        model = DistributedProduct
        fields = [
            'id', 'product', 'quantity', 'employee_name', 'quantity', 'created_at', 'date'
        ]
        ref_name = "DisProductListSerializer"

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "price": obj.product.price,
        }
    