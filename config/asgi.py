import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from core.apps.authentication.websocket.consumers import UserActivationConsumer

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^ws/user_activation/(?P<user_id>\d+)/$', UserActivationConsumer.as_asgi()),
        ])
    ),
})