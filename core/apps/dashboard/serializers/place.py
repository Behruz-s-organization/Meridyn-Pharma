# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Place, District
# accounts
from core.apps.accounts.models import User


class PlaceListSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField(method_name='get_district')
    user = serializers.SerializerMethodField(method_name='get_user')
    
    class Meta:
        model = Place
        fields = [
            'id', 
            'name', 
            'district', 
            'user', 
            'longitude', 
            'latitude', 
            'extra_location', 
            'created_at'
        ]

    def get_district(self, obj):
        return {
            "id": obj.district.id,
            "name": obj.district.name
        }
    
    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name
        }
    

class PlaceCreateSerializer(serializers.Serializer):
    district_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    name = serializers.CharField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    extra_location = serializers.JSONField()

    def validate(self, data):
        district = District.objects.filter(id=data['district_id']).first()
        if not district:
            raise serializers.ValidationError({"district_id": "Tuman topilmadi"})
        
        user = User.objects.filter(id=data['user_id']).first()
        if not user:
            raise serializers.ValidationError({"user_id": "Foydalanuvchi topilmadi"})
        
        data['user'] = user
        data['district'] = district
        return
    
    def create(self, validated_data):
        with transaction.atomic():
            return Place.objects.create(
                name=validated_data.get('name'),
                longitude=validated_data.get('longitude'),
                latitude=validated_data.get('latitude'),
                extra_location=validated_data.get('extra_location'),
                user=validated_data.get('user'),
                district=validated_data.get('district'),
            )
        
    
class PlaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'name', 
            'district', 
            'user', 
            'longitude', 
            'latitude', 
            'extra_location', 
        ]
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.district = validated_data.get('district', instance.district)
            instance.user = validated_data.get('user', instance.user)
            instance.longitude = validated_data.get('longitude', instance.longitude)
            instance.latitude = validated_data.get('latitude', instance.latitude)
            instance.extra_location = validated_data.get('extra_location', instance.extra_location)
            instance.save()
            return instance
