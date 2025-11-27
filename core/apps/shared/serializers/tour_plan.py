from rest_framework import serializers

# shared
from core.apps.shared.models import TourPlan



class TourPlanSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()
    
    class Meta:
        model = TourPlan
        fields = [
            'id', 'place_name', 'longitude', 'latitude', 'location_send', 'created_at'
        ]