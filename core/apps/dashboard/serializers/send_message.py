# rest framework
from rest_framework import serializers


class SendMessageSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())
    message = serializers.CharField()