from rest_framework import serializers

# shared
from core.apps.shared.models import TourPlan



class TourPlanSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()
    
    class Meta:
        model = TourPlan
        fields = [
            'id', 'district', 'longitude', 'latitude', 'created_at'
        ]

    def get_district(self, obj):
        return {
            'id': obj.district.id,
            'name': obj.district.name,
        }