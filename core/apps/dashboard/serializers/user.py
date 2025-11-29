# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# accounts
from core.apps.accounts.models import User
# shared
from core.apps.shared.models import Region


class UserListSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'region',
            'is_active',
            'telegram_id',
            'created_at'
        ]
    
    def get_region(self, obj):
        return {
            'id': obj.region.id,
            'name': obj.region.name,
        }
    

class UserAdminCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    region_id = serializers.IntegerField()
    is_active = serializers.BooleanField()
    telegram_id = serializers.CharField()

    def validate(self, data):
        region = Region.objects.filter(id=data['region_id']).first()
        if not region:
            raise serializers.ValidationError({"region": "Region topilmadi"})
        data['region'] = region
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return User.objects.create(
                username=f"{validated_data.get('first_name')} {validated_data.get('last_name')}",
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                region=validated_data.get('region'),
                is_active=validated_data.get('is_active'),
                telegram_id=validated_data.get('telegram_id'),
            )
        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'region', 'is_active', 'telegram_id'
        ]
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.region = validated_data.get('region', instance.region)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.telegram_id = validated_data.get('telegram_id', instance.telegram_id)
        instance.save()
        return instance