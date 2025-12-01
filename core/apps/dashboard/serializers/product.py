# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# orders
from core.apps.orders.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'created_at'
        ]


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=15)

    def create(self, validated_data):
        with transaction.atomic():
            return Product.objects.create(
                name=validated_data.get('name'),
                price=validated_data.get('price'),
            )
        

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'price'
        ]
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.price = validated_data.get('price', instance.price)
            instance.save()
            return instance
