# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# accounts
from core.apps.accounts.models import User
# shared 
from core.apps.shared.models import Region


class UserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    telegram_id = serializers.CharField()
    region = serializers.IntegerField()

    def validate(self, data):
        if User.objects.filter(username=data['telegram_id']).exists():
            raise serializers.ValidationError("User mavjud")
        region = Region.objects.filter(id=data['region']).first()
        if not region:
            raise serializers.ValidationError({"region": "Region topilmadi"})
        data['region_obj'] = region
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                telegram_id=validated_data.get('telegram_id'),
                region=validated_data.get('region_obj'),
                is_active=False,
                username=validated_data.get('telegram_id'),
            )
            user.region.users_count += 1
            user.region.save()
            return user 
