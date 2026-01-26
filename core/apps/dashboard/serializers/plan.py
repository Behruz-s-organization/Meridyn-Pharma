# django
from django.db import transaction

# rest framework
from rest_framework import serializers

# shared
from core.apps.shared.models import Plan, Doctor, Pharmacy
# accounts
from core.apps.accounts.models import User


class PlanListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    doctor = serializers.SerializerMethodField(method_name='get_doctor')
    pharmacy = serializers.SerializerMethodField(method_name='get_pharmacy')

    class Meta:
        model = Plan
        fields = [
            'id', 
            'title', 
            'description', 
            'date',
            'comment', 
            'doctor', 
            'pharmacy',
            'user',
            'longitude', 
            'latitude', 
            'extra_location',
            'created_at',
        ]
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
        }
    
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


class AdminPlanCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField()
    date = serializers.DateField()
    user_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField(required=False, allow_null=True)
    pharmacy_id = serializers.IntegerField(required=False, allow_null=True)

    longitude = serializers.FloatField(required=False, default=0.0)
    latitude = serializers.FloatField(required=False, default=0.0)
    extra_location = serializers.JSONField(required=False, allow_null=True)


    def validate(self, data):
        user = User.objects.filter(id=data['user_id']).first()
        if not user:
            raise serializers.ValidationError({"user_id": "Foydalanuvchi topilmadi"})
        data['user'] = user
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
            return Plan.objects.create(
                title=validated_data.get('title'),
                description=validated_data.get('description'),
                user=validated_data.get('user'),
                date=validated_data.get('date'),
                doctor=validated_data.get('doctor'),
                pharmacy=validated_data.get('pharmacy'),
                longitude=validated_data.get('longitude'),
                latitude=validated_data.get('latitude'),
                extra_location=validated_data.get('extra_location'),
            )


class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'title', 'description', 'date',
            'comment', 'doctor', 'pharmacy',
            'longitude', 'latitude', 'extra_location',
        ]
    extra_kwargs = {
        "user": {"required": False},
        'title': {"required": False},
    }
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            for field, value in validated_data.items():
                setattr(instance, field, value)
            instance.save()
            return instance
        