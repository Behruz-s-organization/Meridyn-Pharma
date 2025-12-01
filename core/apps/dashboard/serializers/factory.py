# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Factory


class FactoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = [
            'id', 'name', 'created_at'
        ]


class FactoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            return Factory.objects.create(
                name=validated_data.get('name'),
            )
        

class FactoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = [
            'name',
        ]
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance
