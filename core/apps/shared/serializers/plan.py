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