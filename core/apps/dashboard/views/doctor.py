# django
from django.shortcuts import get_object_or_404
from django.db.models import Q

# rest framework
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# dashboard
from core.apps.dashboard.serializers import doctor as serializers

# shared
from core.apps.shared.models import Doctor
from core.apps.shared.utils.response_mixin import ResponseMixin


class DoctorViewSet(viewsets.GenericViewSet, ResponseMixin):
    permission_classes = [permissions.IsAdminUser]
    queryset = Doctor.objects.all()

    def get_serializer_class(self):
        if self.action == "post": 
            return serializers.DoctorCreateSerializer
        elif self.action in ("patch", "put"):
            return serializers.DoctorUpdateSerializer
        else:
            return serializers.DoctorListSerializer

    @swagger_auto_schema(
        tags=['Admin Doctors'],
        manual_parameters=[
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="full_name",
                description="shiforkor ism va familiyasi bo'yicha qidirish",
                required=False,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="district_name",
                description="tuman nomi bo'yicha qidirish",
                required=False,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="place_name",
                description="obyekt bo'yicha qidirish",
                required=False,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="work_place",
                description="ish joyi bo'yicha qidirish",
                required=False,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="sphere",
                description="lavozimi bo'yicha qidirish",
                required=False,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="user",
                description="qo'shgan foydalanuvchini ism va familiyasi bo'yicha qidirish",
                required=False,
                type=openapi.TYPE_STRING,
            ),
        ],
        operation_description="Shifokorlar ro'yxatini olish",
        operation_summary="Shifokolar ro'yxati",
        responses={
            200: openapi.Response(
                schema=None,
                description="Success",
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "malumotlar fetch qilindi",
                        "data": {
                            "count": 0,
                            "next": "string",
                            "pervious": "string",
                            "response": [
                                {
                                    "id": 0,
                                    "first_name": "string",
                                    "last_name": "string",
                                    "phone_number": "string",
                                    "work_place": "string",
                                    "sphere": "string",
                                    "description": "string",
                                    "district": {
                                        "id": 0,
                                        "name": "string",
                                    },
                                    "place": {
                                        "id": 0,
                                        "name": "string"
                                    },
                                    "user": {
                                        'id': 0,
                                        'first_name': "string",
                                        'last_name': "string",
                                    },
                                    "longitude": 0.0,
                                    "latitude": 0.0,
                                    "extra_location": {},
                                    "created_at": "string"
                                }
                            ]
                        }
                    }
                }
            ),
            500: openapi.Response(
                schema=None,
                description="Server Error",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "success": "error",
                        "message": "xatolik",
                        "data": "string"
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['get'], url_path="list")
    def get(self, request):
        try:
            # params
            full_name = request.query_params.get('full_name', None)
            district_name = request.query_params.get('district_name', None)
            place_name = request.query_params.get('place_name', None)
            work_place = request.query_params.get('work_place', None)
            sphere = request.query_params.get('sphere', None)
            user_full_name = request.query_params.get('user', None)

            queryset = self.queryset.all()

            # filters
            if full_name is not None:
                queryset = queryset.filter(
                    Q(first_name__istartswith=full_name) |
                    Q(last_name__istartswith=full_name) 
                )
            if district_name is not None:
                queryset = queryset.filter(
                    district__name__istartswith=district_name
                )
            if place_name is not None:
                queryset = queryset.filter(
                    place__name__istartswith=place_name
                )
            if work_place is not None:
                queryset = queryset.filter(
                    work_place__istartswith=work_place
                )
            if sphere is not None:
                queryset = queryset.filter(
                    sphere__istartswith=sphere
                )
            if user_full_name is not None:
                queryset = queryset.filter(
                    Q(user__first_name__istartswith=user_full_name) |
                    Q(user__last_name__istartswith=user_full_name) 
                )

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.success_response(
                    data=self.get_paginated_response(serializer.data).data,
                    message='malumotlar fetch qilindi'
                )
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(
                data=serializer.data,
                message='malumotlar fetch qilindi'
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )

    @swagger_auto_schema(
        tags=['Admin Doctors']
    )
    @action(detail=False, methods=['post'], url_path='create')
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.DoctorListSerializer(obj).data,
                    message='malumot qoshildi'
                )
            return self.failure_response(
                data=serializer.errors,
                message='malumot qoshilmadi'
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
    
    @swagger_auto_schema(
        tags=['Admin Doctors']
    )
    @action(detail=True, methods=['patch'], url_path='update')
    def update_doctor(self, request, pk=None):
        try:
            doctor = Doctor.objects.filter(id=pk).first()
            if not doctor:
                return self.failure_response(
                    data={},
                    message="doctor topilmadi",
                    status_code=404
                )
            serializer = self.get_serializer(data=request.data, instance=doctor)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.DoctorListSerializer(obj).data,
                    message='malumot tahrirlandi'
                )
            return self.failure_response(
                data=serializer.errors,
                message='malumot tahrirlandi'
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
    
    @swagger_auto_schema(
        tags=['Admin Doctors']
    )
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete(self, request, pk=None):
        try:
            doctor = Doctor.objects.filter(id=pk).first()
            if not doctor:
                return self.failure_response(
                    data={},
                    message="doctor topilmadi",
                    status_code=404
                )
            doctor.delete()
            return self.success_response(
                data={},
                message='malumot ochirildi',
                status_code=204
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
    
    