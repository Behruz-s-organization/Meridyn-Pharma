# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Location, UserLocation, District, Place, Doctor, Pharmacy



class LocationListSerializer(serializers.ModelSerializer):
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