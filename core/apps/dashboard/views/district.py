# django
from django.shortcuts import get_object_or_404

# rest framework
from rest_framework import generics, views
from rest_framework.permissions import IsAdminUser

# drf yasg 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import District
from core.apps.shared.utils.response_mixin import ResponseMixin

# dashboard
from core.apps.dashboard.serializers import district as serializers


class DistrictListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = serializers.DistrictListSerializer
    queryset = District.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=["Admin Districts"],
        responses={
            200: openapi.Response(
                description="Success",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "malumotlar fetch qilindi",
                        "data": {
                            "count": 0,
                            "next": "string",
                            "previous": "string",
                            "results": [
                                {
                                    "id": 0,
                                    "name": "string",
                                    "user": {
                                        "id": 0,
                                        "first_name": "string",
                                        "last_name": "string",
                                    },
                                    "created_at": "string"
                                }
                            ] 
                        }
                    },
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "malumotlar fetch qilindi",
                        "data": [
                            {
                                "id": 0,
                                "name": "string",
                                "user": {
                                    "id": 0,
                                    "first_name": "string",
                                    "last_name": "string",
                                },
                                "created_at": "string"
                            },
                        ]
                    }
                }  
            ),
            500: openapi.Response(
                schema=None,
                description="Server Error",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "status": "error",
                        "message": "xatolik",
                        "data": "string"
                    }
                }
            ),
        }
    )
    def get(self, request):
        try:
            query = self.queryset.all()

            page = self.paginate_queryset(queryset=query)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.success_response(
                    data=self.get_paginated_response(serializer.data).data,
                    message="malumotlar fetch qilindi",
                )
            serializer = self.serializer_class(query, many=True)
            return self.success_response(
                data=serializer.data,
                message='malumotlar fetch qilindi'
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message='xatolik'
            )


class DistrictCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = serializers.DistrictCreateSerializer
    queryset = District.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=["Admin Districts"],
        responses={
            200: openapi.Response(
                description="Success",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "malumotlar qoshildi",
                        "data": {
                            "id": 0,
                            "name": "string",
                            "user": {
                                "id": 0,
                                "first_name": "string",
                                "last_name": "string",
                            },
                            "created_at": "string"
                        }
                    },
                }  
            ),
            400: openapi.Response(
                description="Failure",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 400,
                        "status": "failure",
                        "message": "malumotlar qoshilmadi",
                        "data": "string"
                    },
                }  
            ),
            500: openapi.Response(
                schema=None,
                description="Server Error",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "status": "error",
                        "message": "xatolik",
                        "data": "string"
                    }
                }
            ),
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.DistrictListSerializer(obj).data,
                    message="malumot qoshildi",
                    status_code=201,
                )
            else:
                return self.failure_response(
                    data=serializer.errors,
                    message="malumot qoshilmadi",
                )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )


class DistrictUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = serializers.DistrictUpdateSerializer
    queryset = District.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=["Admin Districts"],
        responses={
            200: openapi.Response(
                description="Success",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "malumotlar tahrirlandi",
                        "data": {
                            "id": 0,
                            "name": "string",
                            "user": {
                                "id": 0,
                                "first_name": "string",
                                "last_name": "string",
                            },
                            "created_at": "string"
                        }
                    },
                }  
            ),
            404: openapi.Response(
                description="Failure",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 404,
                        "status": "failure",
                        "message": "malumotlar topilmadi",
                        "data": {}
                    },
                }  
            ),
            400: openapi.Response(
                description="Failure",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 400,
                        "status": "failure",
                        "message": "malumotlar tahrirlanmadi",
                        "data": "string"
                    },
                }  
            ),
            500: openapi.Response(
                schema=None,
                description="Server Error",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "status": "error",
                        "message": "xatolik",
                        "data": "string"
                    }
                }
            ),
        }
    )
    def patch(self, request, id):
        try:
            obj = District.objects.filter(id=id).first()
            if not obj:
                return self.failure_response(
                    data={}, message="malumot topilmadi", status_code=404
                )
            serializer = self.serializer_class(data=request.data, instance=obj)
            if serializer.is_valid():
                updated_obj = serializer.save()
                return self.success_response(
                    data=serializers.DistrictListSerializer(updated_obj).data,
                    message="malumot tahrirlandi",
                )
            return self.failure_response(
                data=serializer.errors,
                message="malumot tahrirlanmadi"
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )


class DistrictDeleteApiView(views.APIView, ResponseMixin):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=["Admin Districts"],
        responses={
            204: openapi.Response(
                description="Success",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "malumotlar ochirildi",
                        "data": {}
                    },
                }  
            ),
            404: openapi.Response(
                description="Failure",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 404,
                        "status": "failure",
                        "message": "malumotlar topilmadi",
                        "data": {}
                    },
                }  
            ),
            500: openapi.Response(
                schema=None,
                description="Server Error",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "status": "error",
                        "message": "xatolik",
                        "data": "string"
                    }
                }
            ),
        }
    )
    def delete(self, request, id):
        try:
            obj = District.objects.filter(id=id).first()
            if not obj:
                return self.failure_response(
                    data={}, message="malumot topilmadi", status_code=404
                )
            obj.delete()
            return self.success_response(
                    data={},
                    message="malumot ochirildi",
                    status_code=204
                )
        except Exception as e:
            return self.error_response(
                data=str(e), 
                message='xatolik'
            )
