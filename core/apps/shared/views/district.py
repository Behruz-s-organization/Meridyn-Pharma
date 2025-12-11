# django
from django.shortcuts import get_object_or_404

# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import District
from core.apps.shared.serializers import base as base_serializers
from core.apps.shared.serializers import district as district_serializers
from core.apps.shared.utils.response_mixin import ResponseMixin


class DistrictListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = district_serializers.DistrictSerializer
    queryset = District.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: base_serializers.SuccessResponseSerializer(data_serializer=district_serializers.DistrictSerializer()),
            400: base_serializers.BaseResponseSerializer(),
            500: base_serializers.BaseResponseSerializer(),
        }
    )
    def get(self, request):
        try:
            queryset = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return self.success_response(data=serializer.data, message='malumotlar fetch qilindi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')



class DistrictCreateApiView(generics.CreateAPIView, ResponseMixin):
    serializer_class = district_serializers.DistrictSerializer
    queryset = District.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            201: base_serializers.SuccessResponseSerializer(data_serializer=district_serializers.DistrictSerializer()),
            400: base_serializers.BaseResponseSerializer(),
            500: base_serializers.BaseResponseSerializer(),
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                if District.objects.filter(name=name, user=request.user).exists():
                    return self.failure_response(message="District qo'shib bolmadi")
                
                obj = District.objects.create(name=name, user=request.user)
                return self.success_response(
                    data=district_serializers.DistrictSerializer(obj).data,
                    message='malumot qoshildi', 
                    status_code=201
                )
            return self.failure_response(data=serializer.errors, message='malumot qoshilmadi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        
    
class DistrictDeleteUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = district_serializers.DistrictSerializer
    queryset = District.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: base_serializers.SuccessResponseSerializer(),
            400: base_serializers.BaseResponseSerializer(),
            500: base_serializers.BaseResponseSerializer(),
        }
    )
    def patch(self, request, id):
        try:
            obj = get_object_or_404(District, id=id, user=request.user)
            serializer = self.serializer_class(data=request.data, instance=obj)
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                obj.name = name 
                obj.save()
                return self.success_response(
                    data=district_serializers.DistrictSerializer(obj).data,
                    message='Malumot tahrilandi'
                )
            return self.failure_response(
                data=serializer.errors,
                message='Malumot tahrirlanmadi'
            )
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')

    
    @swagger_auto_schema(
        responses={
            204: base_serializers.SuccessResponseSerializer(),
            400: base_serializers.BaseResponseSerializer(),
            500: base_serializers.BaseResponseSerializer(),
        }
    )
    def delete(self, request, id):
        try:
            obj = get_object_or_404(District, id=id, user=request.user)
            obj.delete()
            return self.success_response(message='Malumot ochirildi', status_code=204)
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
