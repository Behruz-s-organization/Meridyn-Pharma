# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Support, District


class SupportCreateSerializer(serializers.Serializer):
    district_id = serializers.IntegerField()
    problem = serializers.CharField()
    date = serializers.DateField()
    type = serializers.ChoiceField(choices=Support.TYPE)

    def validate(self, data):
        district = District.objects.filter(id=data['district_id']).first()
        if not district:
            raise serializers.ValidationError({'district': "district not found"})
        data['district'] = district
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            return Support.objects.create(
                user=self.context.get('user'),
                district=validated_data.get('district'),
                date=validated_data.get('date'),
                type=validated_data.get('type'),
                problem=validated_data.get('problem'    )
            )
