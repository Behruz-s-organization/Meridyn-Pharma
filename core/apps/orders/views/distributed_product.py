# rest framework
from rest_framework import generics, permissions

# orders
from core.apps.orders.models import DistributedProduct
from core.apps.orders.serializers.distributed_product import DistributedProductCreateSerializer

# shared 
from core.apps.shared.utils.response_mixin import ResponseMixin


class DistributedProductCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = DistributedProductCreateSerializer
    queryset = DistributedProduct.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return self.success_response(
                    data={},
                    message="form created",
                    status_code=201
                )
            return self.failure_response(
                data={},
                message="yuborilmadi, iltimos kiritayotgan malumotingizni tekshirib koring",
            )
            
        except Exception as e:
            return self.failure_response(
                data=str(e),
                message="xatolik, backend dasturchiga murojaat qiling"
            )
        