# django
from django.shortcuts import get_object_or_404
from django.db.models import Q

# rest framework
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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

            if search:
                queryset = queryset.filter(
                    Q(first_name__istartswith=search) | 
                    Q(last_name__istartswith=search)
                )
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