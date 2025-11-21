# rest framework
from rest_framework import generics
# rest framework simple jwt
from rest_framework_simplejwt.tokens import RefreshToken
# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer
# accounts
from core.apps.accounts.models import User
# authentication
from core.apps.authentication.serializers.login import LoginSerializer
from core.apps.authentication.serializers import response as response_serializers


class LoginApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        responses={
            200: SuccessResponseSerializer(data_serializer=response_serializers.LoginResponseSerializer()),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                telegram_id = serializer.validated_data.get('telegram_id')
                user = User.objects.filter(telegram_id=telegram_id).first()
                if not user:
                    return self.failure_response(message="User topilmadi")
                if not user.is_active:
                    return self.failure_response(message="User tasdiqlanmagan")

                token = RefreshToken.for_user(user)
                return self.success_response(data={'token': str(token.access_token)})

            return self.failure_response(data=serializer.errors, message='siz tarafdan xatolik')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')