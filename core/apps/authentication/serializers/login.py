from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()