import json

# channels
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

# accounts
from core.apps.accounts.models import User


class UserActivationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs'].get('user_id')
        if self.user_id:
            await self.channel_layer.group_add(
                f"user_{self.user_id}",
                self.channel_name
            )
            await self.accept()
            print(f"User {self.user_id} ulandi")
        else:
            await self.close()
    
    async def disconnect(self, code):
        if self.user_id:
            await self.channel_layer.group_discard(
                f"user_{self.user_id}",
                self.channel_name,
            )
            print(f'User {self.user_id} uzilib ketti')

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'ping':
            await self.send(text_data=json.dumps(
                {
                    'type': 'pong',
                    'message': "boglanish faol"
                }
            ))

    async def user_activated(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_activated',
            'message': 'user aktive qilindi',
            'timestamp': event.get('timestamp'),
            'status': "success",
            "status_code": 200,
            "status_message": "user_activated",
            "token": event.get('token'),
        }))

    