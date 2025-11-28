# rest framework
from rest_framework import generics

# rest framework simple jwt
from rest_framework_simplejwt.tokens import RefreshToken

# drf yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# shared
from core.apps.shared.utils.response_mixin import ResponseMixin
# accounts
from core.apps.accounts.models import User
# authentication
from core.apps.authentication.serializers.login import LoginSerializer, AdminLoginSerializer


class LoginApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary="Login",
        responses={
            200: openapi.Response(
                description="Success",
                schema=None,
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "User topildi",
                        "data": {
                            "id": 1,
                            "first_name": "Behruz",
                            "last_name": "Xoliqberdiyev",
                            "region": "nbve",
                            "is_active": True,
                            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                        }
                    }
                }
            )
        }
    )
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
                user_data['token'] = str(token.access_token)
                return self.success_response(data=user_data, message='User topildi')

            return self.failure_response(data=serializer.errors, message='siz tarafdan xatolik')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        


class AdminLoginApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = AdminLoginSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description="Admin uchun login api",
        responses={
            200: openapi.Response(
                schema=None,
                description="Success",
                examples={
                    "application/json": {
                        "status_code": 200,
                        "success": "success",
                        "message": "Login muvaffaqiyalit amalga oshirildi",
                        "data": {
                            "token": "4jh4j3rbj2fkjb3kfjbwkfjb24kgjb34kgj3kjbkw..."
                        }
                    }
                }
            ),
            404: openapi.Response(
                schema=None,
                description="User not found",
                examples={
                    "application/json": {
                        "status_code": 404,
                        "success": "failure",
                        "message": "username yoki parol notog'ri",
                        "data": {}
                    }
                }
            ),
            400: openapi.Response(
                schema=None,
                description="Failue error",
                examples={
                    "application/json": {
                        "status_code": 400,
                        "success": "failure",
                        "message": "foydalanuvchi aktive emas",
                        "data": {},
                    }
                }
            ),
            500: openapi.Response(
                schema=None,
                description="Server Error",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "success": "error",
                        "message": "xatolik",
                        "data": "some error...",
                    }
                }
            )
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')
                user = User.objects.filter(username=username).first()
                if not user or (user and not user.check_password(password)):
                    return self.failure_response(message="username yoki parol notog'ri", data={}, status_code=404)
                if not user.is_active:
                    return self.failure_response(message="foydalanuvchi aktive emas", data={})

                token = RefreshToken.for_user(user)
                return self.success_response(
                    message="Login muvaffaqiyalit amalga oshirildi",
                    data={"token": str(token.access_token)}
                )

        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')