# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# orders
from core.apps.orders.models import DistributedProduct, Product


class DistributedProductCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    date = serializers.DateField()
    employee_name = serializers.CharField()
    quantity = serializers.IntegerField()
    
    def validate(self, data):
        product = Product.objects.filter(id=data['product_id']).first()
        if not product:
            raise serializers.ValidationError({'product': "product not found"})
        data['product'] = product
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return DistributedProduct.objects.create(
                product=validated_data.get('product'),
                date=validated_data.get('date'),
                employee_name=validated_data.get('employee_name'),
                quantity=validated_data.get('quantity'),
                user=self.context.get('user'),
            )