from rest_framework import serializers


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(required=False, allow_null=True)