# django
from django.db.models import Q

# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# orders
from core.apps.orders.models import DistributedProduct

# shared
from core.apps.shared.utils.response_mixin import ResponseMixin

# dashboard
from core.apps.dashboard.serializers.dis_product import DistributedProductListSerializer


class DistributedProductListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = DistributedProductListSerializer
    queryset = DistributedProduct.objects.all()
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        tags=['Admin Orders'],
        manual_parameters=[
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="product",
                description="product name bo'yicha filter",
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
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="date",
                description="date bo'yicha qidirish",
                required=False,
                type=openapi.FORMAT_DATE,
            ),
        ],
    )
    def get(self, request):
        try:
            product_name = request.query_params.get('product', None)
            date = request.query_params.get('date', None)
            user_full_name = request.query_params.get('user', None)
            
            queryset = self.queryset.all()

            # filters
            if product_name is not None:
                queryset = queryset.filter(product__name__istartswith=product_name)

            if user_full_name is not None:
                queryset = queryset.filter(
                    Q(user__first_name__istartswith=user_full_name) |
                    Q(user__last_name__istartswith=user_full_name) 
                )

            if date is not None:
                queryset = queryset.filter(date=date)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.success_response(
                    data=self.get_paginated_response(serializer.data).data,
                    message="Malumotlar fetch qilindi",
                )
            serializer = self.serializer_class(queryset, many=True)
            return self.success_response(
                data=serializer.data,
                message='Malumotlar fetch qilindi'
            )

        except Exception as e:
            return self.error_response(
                data=str(e),
                message='xatolik, iltimos backend dasturchiga murojaat qiling'
            )