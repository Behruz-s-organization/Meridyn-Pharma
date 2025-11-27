# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import Factory
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.factory import FactorySerializer


class FactoryListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["Farmaseftika"],
        operation_description='Farmasevtikani listini olish uchun api',
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Nomi boyicha qidirish',
                type=openapi.TYPE_STRING,
                required=False,
            )
        ],
        responses={
            200: openapi.Response(
                schema=None,
                description='Success',
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "malumotlar fetch qilindi",
                        "data": [
                            {
                                "id": 0,
                                "name": "string",
                                "created_at": "string",
                            }
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
                        "status": "success",
                        "message": "xatolik",
                        "data": "string",
                    }
                }
            ),
        }
    )
    def get(self, request):
        try:
            query = self.queryset.order_by('-created_at')
            search = request.query_params.get('search')
            if search:
                query = query.filter(name__istartswith=search)

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
