# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Location, UserLocation



class LocationListSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField(method_name='get_district')
    place = serializers.SerializerMethodField(method_name='get_place')
    doctor = serializers.SerializerMethodField(method_name='get_doctor')
    pharmacy = serializers.SerializerMethodField(method_name='get_pharmacy')
    
    class Meta:
        model = Location
        fields = [
            'id', 'longitude', 'latitude', 'created_at', 
            'district', 'place', 'doctor', 'pharmacy', 'updated_at'
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
    


class UserLocationListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user') 

    class Meta:
        model = UserLocation
        fields = [
            'id', 'longitude', 'latitude', 'user', 'created_at', 
        ]

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name
        }