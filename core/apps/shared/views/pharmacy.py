# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import Pharmacy
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.base import SuccessResponseSerializer, BaseResponseSerializer
from core.apps.shared.serializers.pharmacy import PharmacyCreateSerializer, PharmacySerializer


class PharmacyListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = PharmacySerializer
    queryset = Pharmacy.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: SuccessResponseSerializer(data_serializer=PharmacySerializer()),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer()
        }
    )
    def get(self, request):
        try:
            queryset = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return self.success_response(data=serializer.data, message='malumotlar fetch qilindi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')


class PharmacyCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = PharmacyCreateSerializer
    queryset = Pharmacy.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            201: SuccessResponseSerializer(data_serializer=PharmacySerializer()),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer()
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                obj = serializer.save()
                created_data = PharmacySerializer(obj).data
                return self.success_response(data=created_data, message='malumot qoshildi', status_code=201)
            return self.failure_response(data=serializer.errors, message='malumot qoshilmadi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
