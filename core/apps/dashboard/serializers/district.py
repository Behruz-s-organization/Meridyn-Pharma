# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import District
# accounts
from core.apps.accounts.models import User


class DistrictListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = [
            'id', 'name', 'user', 'created_at'
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "telegram_id": obj.user.telegram_id,
        }
    

class DistrictCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        user = User.objects.filter(id=data['user_id']).first()
        if not user:
            raise serializers.ValidationError({"user_id": "Foydalanuvchi topilmadi"})
        data['user'] = user
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return District.objects.create(
                name=validated_data.get('name'),
                user=validated_data.get('user'),
            )
        

class DistrictUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'name', 'user'
        ]
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.user = validated_data.get('user', instance.user)
            instance.save()
            return instance
