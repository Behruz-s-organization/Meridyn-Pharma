# rest framework
from rest_framework import generics, permissions

# drf yasg 
from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi

# accounts
from core.apps.accounts.models import User
from core.apps.accounts.serializers import user as serializers
from core.apps.dashboard.serializers.user import UserListSerializer

# shared
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer


class RegisterUserApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = serializers.UserCreateSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description='Create User',
        responses={
            200: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.success_response(message='Foydalanuvchi qoshildi', status_code=201)
            return self.failure_response(data=serializer.errors, message='Foydalanuvchi qoshilmadi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        

class GetMeApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return self.success_response(
            data=serializer.data
        )
