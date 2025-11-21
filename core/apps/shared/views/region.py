# rest framework
from rest_framework import generics

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.region import RegionSerializer
from core.apps.shared.models import Region
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer



class RegionListApiView(generics.ListAPIView, ResponseMixin):
    serializer_class = RegionSerializer
    queryset = Region.objects.order_by('name')
    pagination_class = None

    @swagger_auto_schema(
        operation_description="Get region list",
        responses={
            200: SuccessResponseSerializer(data_serializer=RegionSerializer()),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        },
        
    )
    def get(self, request):
        try:
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return self.success_response(data=serializer.data, message="malumotlar fetch qilindi")
        except Exception as e:
            return self.error_response(data=str(e), message="malumotlarni fetch qilishda xatolik")