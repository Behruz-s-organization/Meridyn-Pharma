# django
from django.shortcuts import get_object_or_404

# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# orders
from core.apps.orders.models import Order, OrderItem
from core.apps.orders.serializers.order import OrderCreateSerializer, OrderListSerializer, OrderUpdateSerializer
# shared
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer


class OrderCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()
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
                serializer.save()
                return self.success_response(message='malumot qoshildi', status_code=201)
            return self.failure_response(data=serializer.errors, message='malumot qoshilmadi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')


class OrderListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def get(self, request):
        try:
            queryset = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return self.success_response(data=serializer.data, message='malumotlar fetch qilindi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')


class OrderUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = OrderUpdateSerializer
    queryset = Order.objects.all()
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
            obj = get_object_or_404(Order, id=id, user=request.user)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                paid_price = serializer.validated_data.get('paid_price')
                obj.paid_price = paid_price
                obj.save()
                return self.success_response(
                    data=OrderListSerializer(obj).data,
                    message='malumot tahrirlandi'
                )
            return self.failure_response(
                data=serializer.errors,
                message='malumot tahrirlanmadi'
            )

        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')