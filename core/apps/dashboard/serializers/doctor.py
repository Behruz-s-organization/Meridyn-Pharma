# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Doctor
# accounts
from core.apps.accounts.models import User


class DoctorListSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField(method_name='get_district')
    place = serializers.SerializerMethodField(method_name='get_place')
    user = serializers.SerializerMethodField(method_name='get_user')
    
    class Meta:
        model = Doctor
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'work_place',
            'sphere',
            'description',
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
    


class DoctorCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    work_place = serializers.CharField()
    sphere = serializers.CharField()
    description = serializers.CharField()
    district_id = serializers.IntegerField()
    place_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    extra_location = serializers.JSONField()

    def validate(self, data):
        district = ...
        if not district:
            raise serializers.ValidationError({"district_id": "Tuman topilmadi"})
        
        place = ...
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
            return Doctor.objects.create(
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                phone_number=validated_data.get('phone_number'),
                work_place=validated_data.get('work_place'),
                sphere=validated_data.get('sphere'),
                description=validated_data.get('description'),
                district=validated_data.get('district'),
                user=validated_data.get('user'),
                place=validated_data.get('place'),
                longitude=validated_data.get('longitude'),
                latitude=validated_data.get('latitude'),
                extra_location=validated_data.get('extra_location'),
            )


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'work_place',
            'sphere',
            'description',
            'district',
            'place',
            'user',
            'longitude',
            'latitude',
            'extra_location',
        ]

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
            instance.work_place = validated_data.get('work_place', instance.work_place)
            instance.sphere = validated_data.get('sphere', instance.sphere)
            instance.description = validated_data.get('description', instance.description)
            instance.user = validated_data.get('user', instance.user)
            instance.district = validated_data.get('district', instance.district)
            instance.place = validated_data.get('place', instance.place)
            instance.longitude = validated_data.get('longitude', instance.longitude)
            instance.latitude = validated_data.get('latitude', instance.latitude)
            instance.extra_location = validated_data.get('extra_location', instance.extra_location)
            instance.save()
            return instance