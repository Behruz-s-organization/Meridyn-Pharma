# django
from django.shortcuts import get_object_or_404

# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import Doctor
from core.apps.shared.serializers.doctor import DoctorCreateUpdateSerializer, DoctorListSerializer
from core.apps.shared.serializers.base import SuccessResponseSerializer, BaseResponseSerializer
from core.apps.shared.utils.response_mixin import ResponseMixin



class DoctorListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = DoctorListSerializer
    queryset = Doctor.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    @swagger_auto_schema(
        responses={
            200: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def get(self, request):
        try:
            query = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(query, many=True)
            return self.success_response(data=serializer.data, message='malumotlar fetch qilindi')
        except Exception as e:
            return self.error_response(
                data=str(e), message='xatolik'
            )
        

class DoctorCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = DoctorCreateUpdateSerializer
    queryset = Doctor.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            201: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=DoctorListSerializer(obj).data,
                    message="malumot qoshildi"
                )
            return self.failure_response(
                    data=serializer.data,
                    message="malumot qoshilmadi"
            )
        except Exception as e:
            return self.error_response(data=str(e), message='xatolar')
        


class DoctorDeleteUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = DoctorCreateUpdateSerializer
    queryset = Doctor.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def patch(self, request, id):
        try:
            obj = get_object_or_404(Doctor, id=id, user=request.user)
            serializer = self.serializer_class(data=request.data, instance=obj)
            if serializer.is_valid():
                serializer.save()
                return self.success_response(
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
            204: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def delete(self, request, id):
        try:
            obj = get_object_or_404(Doctor, id=id, user=request.user)
            obj.delete()
            return self.success_response(message='Malumot ochirildi', status_code=204)
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
