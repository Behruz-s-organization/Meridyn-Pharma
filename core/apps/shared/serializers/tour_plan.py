# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import TourPlan



class TourPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPlan
        fields = [
            'id', 'place_name', 'longitude', 'latitude', 'location_send', 'date', 'created_at'
        ]


class TourPlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPlan
        fields = [
            'longitude', 'latitude'
        ]

    def update(self, instance, validated_data):
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.save()
        return instance
    

class TourPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPlan
        fields = [
            'place_name', 'date'
        ]
        ref_name = 'CreateTourPlanInWebApp'

    def create(self, validated_data):
        with transaction.atomic():
            return TourPlan.objects.create(
                place_name=validated_data.get('place_name'),
                date=validated_data.get('date'),
                user=self.context.get("user"),
            )
