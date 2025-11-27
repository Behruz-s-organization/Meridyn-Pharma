import os

# packages
import requests

# django
from django.conf import settings
from django.shortcuts import get_object_or_404

# orders
from core.apps.orders.models import Order


def send_to_telegram(chat_id, order_id):
    bot_token = settings.BOT_TOKEN

    try:
        order = get_object_or_404(Order, id=order_id)

        if order.file:
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

            with open(order.file.path, "rb") as pdf:
                files = {'document': pdf}
                data = {'chat_id': chat_id}

                response = requests.post(url, data=data, files=files)

            return True

    except Exception as e:
        print(f"Telegram xatolik: {e}")
        return False