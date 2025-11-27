import os

# packages
import requests

# django
from django.conf import settings


def send_to_telegram(chat_id, file_path=None):
    bot_token = settings.BOT_TOKEN

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": "Buyurtma uchun yuklangan PDF file",
            "parse_mode": "HTML"
        }

        if file_path and os.path.exists(file_path):
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': chat_id}
                requests.post(url, files=files, data=data)
            
        return True
    except Exception as e:
        print(f"Telegram xatolik: {e}")
        return False

