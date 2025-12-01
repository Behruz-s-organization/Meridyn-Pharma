# django
from django.shortcuts import get_object_or_404

# rest framework
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

# drf yasg 
from drf_yasg.utils import swagger_auto_schema

# orders
from core.apps.orders.models import Payment
# shared
from core.apps.shared.utils.response_mixin import ResponseMixin
# dashboard
from core.apps.dashboard.serializers import payment as serializers


class PaymentListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = serializers.PaymentListSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=["Admin Orders"],
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