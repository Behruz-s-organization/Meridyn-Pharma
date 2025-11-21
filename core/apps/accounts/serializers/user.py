# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# accounts
from core.apps.accounts.models import User
# shared 
from core.apps.shared.models import Region


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'telegram_id', 'region'
        ]

    def validate(self, data):
        if User.objects.filter(username=data['telegram_id']).exists():
            raise serializers.ValidationError("User mavjud")
        region = Region.objects.filter(id=data['region']).first()
        if not region:
            raise serializers.ValidationError("Region topilmadi")
        data['region'] = region
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                telegram_id=validated_data.get('telegram_id'),
                region=validated_data.get('region'),
                is_active=False,
                username=validated_data.get('telegram_id'),
            )
            user.region.users_count += 1
            user.region.save()
            return user 
