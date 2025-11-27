# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Doctor, District, Place
# accounts 
from core.apps.accounts.models import User


class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id', 
            'first_name',
            'last_name',
            'phone_number',
            'work_place',
            'description',
            'sphere',
            'district',
            'place',
            'longitude',
            'latitude',
            'extra_location',
            'created_at', 
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


class DoctorCreateUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    work_place = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    district = serializers.IntegerField(required=False)
    place = serializers.IntegerField(required=False)
    longitude = serializers.FloatField(required=False)
    latitude = serializers.FloatField(required=False)
    extra_location = serializers.JSONField(required=False)
    sphere = serializers.CharField()

    def validate(self, data):
        if data.get('district'):
            district = District.objects.filter(id=data['district']).first()
            if not district:
                raise serializers.ValidationError({"district": "District topilamadi"})
            data['district_obj'] = district
        if data.get('place'):
            place = Place.objects.filter(id=data['place']).first()
            if not place:
                raise serializers.ValidationError({"place": "Place topilamadi"})
            data['place_obj'] = place
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return Doctor.objects.create(
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                phone_number=validated_data.get('phone_number'),
                work_place=validated_data.get('work_place'),
                description=validated_data.get('description'),
                district=validated_data.get('district_obj'),
                place=validated_data.get('place_obj'),
                longitude=validated_data.get('longitude'),
                latitude=validated_data.get('latitude'),
                extra_location=validated_data.get('extra_location'),   
                user=self.context.get('user'),
                sphere=validated_data.get('sphere'),
            )
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
            instance.work_place = validated_data.get('work_place', instance.work_place)
            instance.description = validated_data.get('description', instance.description)
            instance.district = validated_data.get('district_obj', instance.district)
            instance.place = validated_data.get('place_obj', instance.place)
            instance.longitude = validated_data.get('longitude', instance.longitude)
            instance.latitude = validated_data.get('latitude', instance.latitude)
            instance.extra_location = validated_data.get('extra_location', instance.extra_location)
            instance.sphere = validated_data.get('sphere', instance.sphere)
            instance.save()
            return instance