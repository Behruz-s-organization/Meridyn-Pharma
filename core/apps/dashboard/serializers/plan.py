# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Plan
# accounts
from core.apps.accounts.models import User


class PlanListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    
    class Meta:
        model = Plan
        fields = [
            'id',
            'title',
            'description',
            'date',
            'user',
            'created_at'
        ]
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
        }


class PlanCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    date = serializers.DateField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        user = User.objects.filter(id=data['user_id']).first()
        if not user:
            raise serializers.ValidationError({"user_id": "Foydalanuvchi topilmadi"})
        data['user'] = user
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return Plan.objects.create(
                title=validated_data.get('title'),
                description=validated_data.get('description'),
                user=validated_data.get('user'),
                date=validated_data.get('date'),
            )


class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'title',
            'description',
            'date',
            'user',
        ]
    extra_kwargs = {
        "user": {"required": False}
    }
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.user = validated_data.get('user', instance.user)
            instance.date = validated_data.get('date', instance.date)
            instance.save()
            return instance
    