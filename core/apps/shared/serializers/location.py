# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Location, UserLocation, District, Place, Doctor, Pharmacy



class LocationSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField(method_name='get_district')
    place = serializers.SerializerMethodField(method_name='get_place')
    doctor = serializers.SerializerMethodField(method_name='get_doctor')
    pharmacy = serializers.SerializerMethodField(method_name='get_pharmacy')
    
    class Meta:
        model = Location
        fields = [
            'id', 'longitude', 'latitude', 'created_at', 
            'district', 'place', 'doctor', 'pharmacy',
        ]
    
    def get_district(self, obj):
        return {
            'id': obj.district.id,
            'name': obj.district.name,
        } if obj.district else None
    

    def get_place(self, obj):
        return {
            'id': obj.place.id,
            'name': obj.place.name,
        } if obj.place else None
    
    def get_doctor(self, obj):
        return {
            'id': obj.doctor.id,
            'first_name': obj.doctor.first_name,
            'last_name': obj.doctor.last_name,
        } if obj.doctor else None

    def get_pharmacy(self, obj):
        return {
            'id': obj.pharmacy.id,
            'name': obj.pharmacy.name,
        } if obj.pharmacy else None
    

class CreateLocationSerializer(serializers.Serializer):
    district_id = serializers.IntegerField(required=False)
    place_id = serializers.IntegerField(required=False)
    doctor_id = serializers.IntegerField(required=False)
    pharmacy_id = serializers.IntegerField(required=False)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    def validate(self, data):
        user = self.context.get('user')
        if data.get('district_id'):
            district = District.objects.filter(user=user, id=data['district_id']).first()
            if not district:
                raise serializers.ValidationError({"district_id": "District not found"})
            data['district'] = district

        if data.get('place_id'):
            place = Place.objects.filter(user=user, id=data['place_id']).first()
            if not place:
                raise serializers.ValidationError({"place_id": "Place not found"})
            data['place'] = place

        if data.get('doctor_id'):
            doctor = Doctor.objects.filter(user=user, id=data['doctor_id']).first()
            if not doctor:
                raise serializers.ValidationError({"doctor_id": "Doctor not found"})
            data['doctor'] = doctor
        
        if data.get('pharmacy_id'):
            pharmacy = Pharmacy.objects.filter(user=user, id=data['pharmacy_id']).first()
            if not pharmacy:
                raise serializers.ValidationError({"pharmacy_id": "Pharmacy not found"})
            data['pharmacy'] = pharmacy
        
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            return Location.objects.create(
                district=validated_data.get('district'),
                place=validated_data.get('place'),
                doctor=validated_data.get('doctor'),
                pharmacy=validated_data.get('pharmacy'),
                user=self.context.get('user'),
                longitude=validated_data.get('longitude'),
                latitude=validated_data.get('latitude'),
            )
        

class UserLocationSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    def create(self, validated_data):
        with transaction.atomic():
            return UserLocation.objects.create(
                user=self.context.get('user'),
                longitude=validated_data.get('longitude'),
                latitude=validated_data.get('latitude'),
            )