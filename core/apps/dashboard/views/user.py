from asgiref.sync import async_to_sync
import datetime

# django
from django.shortcuts import get_object_or_404
from django.db.models import Q

# rest framework
from rest_framework import generics, views
from rest_framework.permissions import IsAdminUser

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# rest framework simple jwt
from rest_framework_simplejwt.tokens import RefreshToken

# channels
from channels.layers import get_channel_layer

# dashboard
from core.apps.dashboard.serializers import user as serializers
# accounts
from core.apps.accounts.models import User
# shared
from core.apps.shared.utils.response_mixin import ResponseMixin



class UserListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = serializers.UserListSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search by first_name or last_name',
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name='is_active',
                in_=openapi.IN_QUERY,
                description="holati boyicha filter qilish",
                type=openapi.TYPE_BOOLEAN,
                required=False
            ),
            openapi.Parameter(
                name="region_id",
                in_=openapi.IN_QUERY,
                description="region boyicha filter qilish",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                schema=None,
                description="Foydalanuvchilar ro'yxati",
                examples={
                    "application/json": {
                        "status_code": 200,
                        "success": "success",
                        "message": "Foydalanuvchilar ro'yxati",
                        "data": {
                            "count": 0,
                            "next": "string",
                            "previous": "string",
                            "results": [
                                {
                                    "id": 0,
                                    "first_name": "string",
                                    "last_name": "string",
                                    "region": "string",
                                    "is_active": "true",
                                    "created_at": "2025-11-26T11:07:58.483Z"
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
                        "message": 'xatolik',
                        "data": "some errors..."
                    }
                }
            ),
        }
    )
    def get(self, request):
        try: 
            queryset = self.queryset.exclude(id=request.user.id)
            # filters
            search = request.query_params.get('search')
            is_active = request.query_params.get('is_active', None)
            region_id = request.query_params.get('region_id')

            if search:
                queryset = queryset.filter(
                    Q(first_name__istartswith=search) | 
                    Q(last_name__istartswith=search)
                )
            if is_active is not None:
                queryset = queryset.filter(is_active=True if is_active.lower() == 'true' else False)
            if region_id:
                queryset = queryset.filter(region__id=region_id)

            page = self.paginate_queryset(queryset=queryset)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                paginated_data = self.get_paginated_response(serializer.data)
                return self.success_response(
                    data=paginated_data.data,
                    message="Foydalanuvchilar ro'yxati",
                )
            else:
                serializer = self.serializer_class(queryset, many=True)
                return self.success_response(
                    data=serializer.data,
                    message="Foydalanuvchilar ro'yxati",
                )
        except Exception as e:
            return self.error_response(str(e), message="xatolik")
        

class UserCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = serializers.UserAdminCreateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={
            201: openapi.Response(
                schema=None,
                description="Success",
                examples={
                    "application/json":{
                        "status_code": 201,
                        "status": "success",
                        "message": "Foydalanuvchi qo'shildi",
                        "data": {
                            "id": 0,
                            "first_name": "string",
                            "last_name": "string",
                            "region": {
                                "id": 0,
                                "name": "string",
                            },
                            "is_active": True,
                            "created_at": "string"
                        }
                    }
                }
            ),
            400: openapi.Response(
                schema=None,
                description="Failure",
                examples={
                    "application/json": {
                        "status_code": 400,
                        "status": "failure",
                        "message": "Foydalanuvchi qo'shilmadi",
                        "data": "string",
                    }
                }
            ),
            500: openapi.Response(
                schema=None,
                description="Failure",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "status": "error",
                        "message": "xatolik",
                        "data": "string",
                    }
                }
            ),
        }
    )
    def post(self, request):
        try: 
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                new_user = serializer.save()
                return self.success_response(
                    data=serializers.UserListSerializer(new_user).data,
                    message="Foydalanuvchi qo'shildi",
                    status_code=201
                )

            return self.failure_response(
                data=serializer.errors,
                message="Foydalanuvchi qo'shilmadi",
            )
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        

    
class UserUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = serializers.UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                schema=None,
                description="Success",
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "Foydalanuvchi tahrirlandi",
                        "data": {
                            "id": 0,
                            "first_name": "string",
                            "last_name": "string",
                            "region": {
                                "id": 0,
                                "name": "string"
                            },
                            "is_active": True,
                            "created_at": "string" 
                        }
                    }
                }
            ),
            404: openapi.Response(
                schema=None,
                description="Not Found",
                examples={
                    "application/json": {
                        "status_code": 404,
                        "success": "failure",
                        "message": "Foydalanuvchi topilmadi",
                        "data": {},
                    }
                }
            ),
            400: openapi.Response(
                schema=None,
                description="Failure",
                examples={
                    "application/json": {
                        "status_code": 400,
                        "message": "Foydalanuvchi tahrirlanmadi",
                        "data": {}
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
    def patch(self, request, id):
        try: 
            user = User.objects.filter(id=id).first()
            if not user:
                return self.failure_response(
                    data={}, message="Foydalanuvchi topilmadi", status_code=404
                )
            serializer = self.serializer_class(data=request.data, instance=user)
            if serializer.is_valid():
                updated_user = serializer.save()
                return self.success_response(
                    data=serializers.UserListSerializer(updated_user).data,
                    message="Foydalanuvchi tahrirlandi"
                )
            return self.failure_response(
                data=serializer.errors,
                message="Foydalanuvchi tahrirlanmadi"
            )
        except Exception as e:
            return self.error_response(data=str(e), message="xatolik")
        


class UserDeleteApiView(views.APIView, ResponseMixin):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={
            204: openapi.Response(
                schema=None,
                description="Success",
                examples={
                    "application/json": {
                        "status_code": 204,
                        "status": "success",
                        "message": "Foydalanuvchi o'chirildi",
                        "data": {}
                    }
                }
            ),
            404: openapi.Response(
                schema=None,
                description="Not Found",
                examples={
                    "application/json": {
                        "status_code": 404,
                        "success": "failure",
                        "message": "Foydalanuvchi topilmadi",
                        "data": {},
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
    def delete(self, request, id):
        try:
            user = User.objects.filter(id=id).first()
            if not user:
                return self.failure_response(
                    data={}, 
                    message="Foydalanuvchi topilmadi", 
                    status_code=404
                )
            user.delete()
            return self.success_response(
                data={}, 
                message="Foydalanuvchi o'chirildi",
                status_code=204
            )
        except Exception as e:
            return self.error_response(data=str(e), message="xatolik")
        


class UserActivateApiView(views.APIView, ResponseMixin):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                schema=None,
                description="Success",
                examples={
                    "application/json": {
                        "status_code": 204,
                        "status": "success",
                        "message": "user tasdiqlandi",
                        "data": {
                            "id": 0,
                            "first_name": "string",
                            "last_name": "string",
                            "region": {
                                "id": 0,
                                "name": "string"
                            },
                            "is_active": True,
                            "created_at": "string" 
                        }
                    }
                }
            ),
            404: openapi.Response(
                schema=None,
                description="Not Found",
                examples={
                    "application/json": {
                        "status_code": 404,
                        "success": "failure",
                        "message": "User not found",
                        "data": {},
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
    def post(self, request, id):
        try:
            channel_layer = get_channel_layer()
            user = User.objects.filter(id=id).first()
            if not user:
                return self.failure_response(data={}, message='User not found', status_code=404)
            user.is_active = True
            user.save()
            token = RefreshToken.for_user(user)

            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    'type': 'user_activated',
                    'message': 'user aktive qilindi',
                    'status': "success",
                    "status_code": 200,
                    "status_message": "user_activated",
                    "token": str(token.access_token),
                }
            )
            return self.success_response(
                data=serializers.UserListSerializer(user).data,
                message="user tasdiqlandi",
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message='xatolik'
            )
