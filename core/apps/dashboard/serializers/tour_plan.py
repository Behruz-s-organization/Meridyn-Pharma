# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import TourPlan
# accounts
from core.apps.accounts.models import User


class TourPlanListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = TourPlan
        fields = [
            'id', 'place_name', 'user', 'latitude', 
            'longitude', 'location_send', 'date', 'created_at'
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }


class TourPlanCreateSerializer(serializers.Serializer):
    place_name = serializers.CharField()
    user_id = serializers.IntegerField()
    date = serializers.DateField()

    def validate(self, data):
        user = User.objects.filter(id=data['user_id']).first()
        if not user:
            raise serializers.ValidationError({"user_id": "Foydalanuvchi topilmadi"})
        data['user'] = user
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return TourPlan.objects.create(
                place_name=validated_data.get('place_name'),
                user=validated_data.get('user'),
                date=validated_data.get('date'),
            )
        

class TourPlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPlan
        fields = [
            'place_name', 'user', 'date'
        ]
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.place_name = validated_data.get('place_name', instance.place_name)
            instance.user = validated_data.get('user', instance.user)
            instance.date = validated_data.get('date', instance.date)
            instance.save()
            return instance
