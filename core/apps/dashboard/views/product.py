# django
from django.db.models import Q

# rest framework
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# dashboard
from core.apps.dashboard.serializers import product as serializers
# orders
from core.apps.orders.models import Product
# shared
from core.apps.shared.utils.response_mixin import ResponseMixin


class ProductViewSet(viewsets.GenericViewSet, ResponseMixin):
    permission_classes = [permissions.IsAdminUser]
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "post": 
            return serializers.ProductCreateSerializer
        elif self.action in ["patch", "put"]:
            return serializers.ProductUpdateSerializer
        else:
            return serializers.ProductListSerializer

    @swagger_auto_schema(
        tags=['Admin Products'],
        manual_parameters=[
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="name",
                description="name bo'yicha filter",
                required=False,
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(detail=False, methods=['get'], url_path="list")
    def get(self, request):
        try:
            # params
            name = request.query_params.get('name', None)

            queryset = self.queryset.all()

            # filters
            if name is not None:
                queryset = queryset.filter(name__istartswith=name)
            
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
        tags=['Admin Products']
    )
    @action(detail=False, methods=['post'], url_path='create')
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.ProductListSerializer(obj).data,
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
        tags=['Admin Products']
    )
    @action(detail=True, methods=['patch'], url_path='update')
    def update_doctor(self, request, pk=None):
        try:
            product = Product.objects.filter(id=pk).first()
            if not product:
                return self.failure_response(
                    data={},
                    message="product topilmadi",
                    status_code=404
                )
            serializer = self.get_serializer(data=request.data, instance=product)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.ProductListSerializer(obj).data,
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
        tags=['Admin Products']
    )
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete(self, request, pk=None):
        try:
            product = Product.objects.filter(id=pk).first()
            if not product:
                return self.failure_response(
                    data={},
                    message="product topilmadi",
                    status_code=404
                )
            product.delete()
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
    
    