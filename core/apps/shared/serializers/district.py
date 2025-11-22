from rest_framework import serializers

# shared
from core.apps.shared.models import District


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'id', 'name', 'created_at'
        ]