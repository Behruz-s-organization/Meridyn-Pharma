from rest_framework import serializers

# shared
from core.apps.shared.models import Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            'id', 'name', 'created_at'
        ]