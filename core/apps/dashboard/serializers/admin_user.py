# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# accounts
from core.apps.accounts.models.user import User


class AdminUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'is_superuser'
        ]
        
    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                username=validated_data['username'],
                is_superuser=validated_data['is_superuser'],
                is_staff=True,
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
            

class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'is_superuser', 'is_staff'
        ]
        

class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'is_superuser', 'is_staff'
        ]
        
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance