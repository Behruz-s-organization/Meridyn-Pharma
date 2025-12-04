# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Support


class SupportListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    district = serializers.SerializerMethodField(method_name='get_district')
    
    class Meta:
        model = Support
        fields = [
            'id', 'problem', 'date', 'type', 'district', 'user', 'created_at'
        ]

    def get_district(self, obj):
        return {
            'id': obj.district.id,
            'name': obj.district.name,
        } if obj.district else None
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
        }
    