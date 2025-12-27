# django
from django.db import transaction

# serializers
from rest_framework import serializers

# shared
from core.apps.shared.models import Pharmacy, District, Place



class PharmacySerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()

    class Meta:
        model = Pharmacy
        fields = [
            'id', 'name', 'inn', 'owner_phone', 'responsible_phone',
            'district', 'place', 'longitude', 'latitude', 'extra_location', 'created_at'
        ]

    def get_district(self, obj):
        return {
            'id': obj.district.id,
            'name': obj.district.name,
        }
    
    def get_place(self, obj):
        return {
            'id': obj.place.id,
            'name': obj.place.name,
        }
    

class PharmacyCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    inn = serializers.CharField()
    owner_phone = serializers.CharField(required=False)
    responsible_phone = serializers.CharField(required=False)
    district_id = serializers.IntegerField()
    place_id = serializers.IntegerField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    extra_location = serializers.JSONField()

    def validate(self, data):
        district = District.objects.filter(id=data['district_id']).first()
        if not district:
            raise serializers.ValidationError({"district_id": "District topilmadi"})
        place = Place.objects.filter(id=data['place_id']).first()
        if not place:
            raise serializers.ValidationError({'place_id': "Place topilmadi"})
        
        data['district'] = district
        data['place'] = place
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            return Pharmacy.objects.create(
                name=validated_data.get('name'),
                inn=validated_data.get('inn'),
                owner_phone=validated_data.get('owner_phone'),
                responsible_phone=validated_data.get('responsible_phone'),
                district=validated_data.get('district'),
                place=validated_data.get('place'),
                longitude=validated_data.get('longitude'),
                latitude=validated_data.get('latitude'),
                extra_location=validated_data.get('extra_location'),
                user=self.context.get('user'),
            )