# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id', 'title', 'description', 'date', 'is_done', 'created_at'
        ]

    def create(self, validated_data):
        with transaction.atomic():
            return Plan.objects.create(
                title=validated_data.get('title'),
                description=validated_data.get('description'),
                date=validated_data.get('date'),
                user=self.context.get('user'),
            )
        

class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'title', 'description', 'date', 'is_done',
        ]

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.is_done = validated_data.get('is_done')
        instance.save()
        return instance