# rest framework
from rest_framework import generics, permissions


# services
from core.services.send_telegram_msg import send_message
# accounts
from core.apps.accounts.models import User
#shared
from core.apps.shared.utils.response_mixin import ResponseMixin
# dashboard
from core.apps.dashboard.serializers.send_message import SendMessageSerializer


class SendMessageToEmployee(generics.GenericAPIView, ResponseMixin):
    serializer_class = SendMessageSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                message = data.get('message')
                user_ids = data.get('user_ids')
                users = User.objects.filter(id__in=user_ids)
                for user in users:
                    send_message(chat_id=user.telegram_id, message=message)
                return self.success_response(
                    data={},
                    message="Xabar yuborildi"
                )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik, backend dasturchi bilan boglaning"
            )