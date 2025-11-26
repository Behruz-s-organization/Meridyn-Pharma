from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    