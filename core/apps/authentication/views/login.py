# rest framework
from rest_framework import generics

# rest framework simple jwt
from rest_framework_simplejwt.tokens import RefreshToken

# drf yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

    # @swagger_auto_schema(
    #     operation_summary="Login",
    #     responses={
    #         200: openapi.Response(
    #             description="Success",
    #             schema=openapi.Schema(  
    #                 type=openapi.TYPE_OBJECT
    #             ),
    #             examples={
    #                 "application/json": {
    #                     "status_code": 200,
    #                     "status": "success",
    #                     "message": "User topildi",
    #                     "data": {
    #                         "id": 1,
    #                         "first_name": "Behruz",
    #                         "last_name": "Xoliqberdiyev",
    #                         "region": "nbve",
    #                         "is_active": True,
    #                         "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    #                     }
    #                 }
    #             }
    #         )
    #     }
    # )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                telegram_id = serializer.validated_data.get('telegram_id')
                user = User.objects.filter(telegram_id=telegram_id).first()
                if not user:
                    return self.failure_response(message="User topilmadi", status_code=404)
                user_data = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'region': user.region.name,
                    'is_active': user.is_active,
                    'token': None
                }
                if not user.is_active:
                    return self.success_response(
                        message="User tasdiqlanmagan",
                        data=user_data
                    )

                token = RefreshToken.for_user(user)
                user_data['token'] = str(token)
                return self.success_response(data=user_data, message='User topildi')

            return self.failure_response(data=serializer.errors, message='siz tarafdan xatolik')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')