# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Plan, Doctor, Pharmacy


class PlanCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    date = serializers.DateField()
    doctor_id = serializers.IntegerField(required=False, allow_null=True)
    pharmacy_id = serializers.IntegerField(required=False, allow_null=True)

    longitude = serializers.FloatField(required=False, default=0.0)
    latitude = serializers.FloatField(required=False, default=0.0)
    extra_location = serializers.JSONField(required=False, allow_null=True)

    def validate(self, data):
        if data.get('doctor_id'):
            doctor = Doctor.objects.filter(id=data.get('doctor_id')).first()
            if not doctor:
                raise serializers.ValidationError({"doctor": "Doctor not found"})
            data['doctor'] = doctor
        if data.get('pharmacy_id'):
            pharmacy = Pharmacy.objects.filter(id=data.get('pharmacy_id')).first()
            if not pharmacy:
                raise serializers.ValidationError({"pharmacy_id": "Pharmacy not found"})
            data['pharmacy'] = pharmacy

        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context['user']
            doctor = validated_data.pop('doctor', None)
            pharmacy = validated_data.pop('pharmacy', None)
            plan = Plan.objects.create(
                user=user,
                doctor=doctor,
                pharmacy=pharmacy,
                **validated_data
            )
            return plan


class PlanSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField(method_name='get_doctor')
    pharmacy = serializers.SerializerMethodField(method_name='get_pharmacy')

    class Meta:
        model = Plan
        fields = [
            'id', 'title', 'description', 'date',
            'comment', 'doctor', 'pharmacy',
            'longitude', 'latitude', 'extra_location',
            'created_at'
        ]
        read_only_fields = ['id', 'is_done', 'created_at']

    def get_doctor(self, obj):
        return {
            "id": obj.doctor.id,
            "first_name": obj.doctor.first_name,
            "last_name": obj.doctor.last_name
        } if obj.doctor is not None else None

    def get_pharmacy(self, obj):
        return {
            "id": obj.pharmacy.id,
            "name": obj.pharmacy.name,
        } if obj.pharmacy is not None else None
    

class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'title', 'description', 'date',
            'comment', 'doctor', 'pharmacy',
            'longitude', 'latitude', 'extra_location',
        ]

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class PlanCompliteSerializer(serializers.Serializer):
    comment = serializers.CharField()