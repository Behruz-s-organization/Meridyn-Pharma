# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Place, District


class PlaceSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = [
            'id', 'name', 'latitude', 'longitude', 'extra_location', 'district', 'created_at'
        ]

    def get_district(self, obj):
        return {
            "id": obj.district.id,
            "name": obj.district.name,
        }


class PlaceCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    extra_location = serializers.JSONField()
    district_id = serializers.IntegerField()
    
    def validate_name(self, value):
        if not Place.objects.filter(name=value).exists():
            raise serializers.ValidationError({"name": "Place bu name bilan mavjud"})
        return value
    
    def validate(self, data):
        district = District.objects.filter(id=data['district_id']).first()
        if not district:
            raise serializers.ValidationError({"district_id": "District not found"})
        data['district'] = district
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return Place.objects.create(
                name=validated_data.get('name'),
                latitude=validated_data.get('latitude'),
                longitude=validated_data.get('longitude'),
                extra_location=validated_data.get('extra_location'),
                district=validated_data.get('district'),
                user=self.context.get('user'),
            )

