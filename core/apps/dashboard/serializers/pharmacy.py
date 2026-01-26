# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Pharmacy, District, Place
# accounts
from core.apps.accounts.models import User


class PharmacyListSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField(method_name='get_district')
    place = serializers.SerializerMethodField(method_name='get_place')
    user = serializers.SerializerMethodField(method_name='get_user')
    
    class Meta:
        model = Pharmacy
        fields = [
            'id',
            'name',
            'inn',
            'owner_phone',
            'responsible_phone',
            'district',
            'place',
            'user',
            'longitude',
            'latitude',
            'extra_location',
            'created_at'
        ]
    
    def get_district(self, obj):
        return {
            'id': obj.district.id,
            'name': obj.district.name
        }
    
    def get_place(self, obj):
        return {
            'id': obj.place.id,
            'name': obj.place.name
        }
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
        }
    


class AdminPharmacyCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    inn = serializers.CharField(required=False)
    owner_phone = serializers.CharField()
    responsible_phone = serializers.CharField()
    district_id = serializers.IntegerField()
    place_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    extra_location = serializers.JSONField()

    def validate(self, data):
        district = District.objects.filter(id=data['district_id']).first()
        if not district:
            raise serializers.ValidationError({"district_id": "Tuman topilmadi"})
        
        place = Place.objects.filter(id=data['place_id']).first()
        if not place:
            raise serializers.ValidationError({'place_id': "Obyekt topilmadi"})
        
        user = User.objects.filter(id=data['user_id']).first()
        if not user:
            raise serializers.ValidationError({"user_id": "Foydalanuvchi topilmadi"})
        data['district'] = district

        data['place'] = place
        data['user'] = user
        return data
    def create(self, validated_data):
        with transaction.atomic():
            return Pharmacy.objects.create(
                name=validated_data.get('name'),
                inn=validated_data.get('inn'),
                owner_phone=validated_data.get('owner_phone'),
                responsible_phone=validated_data.get('responsible_phone'),
                district=validated_data.get('district'),
                user=validated_data.get('user'),
                place=validated_data.get('place'),
                longitude=validated_data.get('longitude'),
                latitude=validated_data.get('latitude'),
                extra_location=validated_data.get('extra_location'),
            )


class PharmacyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = [
            'name',
            'inn',
            'owner_phone',
            'responsible_phone',
            'district',
            'place',
            'user',
            'longitude',
            'latitude',
            'extra_location',
        ]

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.inn = validated_data.get('inn', instance.inn)
            instance.owner_phone = validated_data.get('owner_phone', instance.owner_phone)
            instance.responsible_phone = validated_data.get('responsible_phone', instance.responsible_phone)
            instance.user = validated_data.get('user', instance.user)
            instance.district = validated_data.get('district', instance.district)
            instance.place = validated_data.get('place', instance.place)
            instance.longitude = validated_data.get('longitude', instance.longitude)
            instance.latitude = validated_data.get('latitude', instance.latitude)
            instance.extra_location = validated_data.get('extra_location', instance.extra_location)
            instance.save()
            return instance