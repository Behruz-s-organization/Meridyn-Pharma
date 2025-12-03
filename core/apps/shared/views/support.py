# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import Support
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.support import SupportCreateSerializer


class SupportCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = SupportCreateSerializer
    queryset = Support.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={"user": request.user})
            if serializer.is_valid():
                data = serializer.save()
                return self.success_response(
                    data={},
                    message="Xabar yuborildi",
                    status_code=201
                )
            return self.failure_response(
                data=serializer.errors,
                message='Xabar yuborilmadi, iltimos malumotlar togri ekanligini tekshirib koring',
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message='xatolik, backend dastruchiga murojaat qiling iltimos'
            )