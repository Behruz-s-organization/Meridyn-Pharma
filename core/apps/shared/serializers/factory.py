from rest_framework import serializers


# shared
from core.apps.shared.models import Factory



class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = [
            'id', 'name', 'created_at'
        ]