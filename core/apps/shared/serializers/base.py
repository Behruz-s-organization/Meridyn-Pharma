from rest_framework import serializers


class BaseResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    message = serializers.CharField(required=False, allow_null=True)
    data = serializers.JSONField(required=False, allow_null=True)


class SuccessResponseSerializer(BaseResponseSerializer):
    def __init__(self, data_serializer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if data_serializer:
            self.fields['data'] = data_serializer
        else:
            self.fields['data'] = serializers.JSONField(required=False)