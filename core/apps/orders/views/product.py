from rest_framework import permissions, generics

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# orders
from core.apps.orders.models import Product
from core.apps.orders.serializers.product import ProductSerializer
# shared
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer
from core.apps.shared.utils.response_mixin import ResponseMixin


class ProductApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
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
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return self.success_response(data=serializer.data, message='malumotlar fetch qilindi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
