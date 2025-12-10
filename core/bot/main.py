# python
import asyncio, logging, sys, os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

# aiogram
from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# django
from django.conf import settings

TOKEN = settings.BOT_TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(filters.CommandStart)
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Tizimga kirish",
                web_app=WebAppInfo(url="https://bot.meridynpharma.com")
            )]
        ],
    )
    text = """
    🔐 MeridynPharma ish tizimiga kirish
    
Hurmatli xodim,
MeridynPharma’ning ichki ish jarayonlarini avtomatlashtirish va kunlik faoliyatni samarali boshqarish uchun mo‘ljallangan Rasmiy Xodimlar Mini-Ilovasiga xush kelibsiz.

Ushbu platforma orqali sizga biriktirilgan vazifalar, hisobotlar, inventarizatsiya jarayonlari va ichki eslatmalar yagona tizim orqali boshqariladi.

▶️ Tizimga kirish tartibi

Ish faoliyatini boshlash uchun quyidagi bosqichni bajaring:

1. Quyida joylashgan “Tizimga kirish” tugmasini bosing.
yoki
2. Mini-Ilova ochilgandan so‘ng, mini ilova pastki qismida joylashgan tizimga kirish degan tugmani bosing

Agar mini-app avtomatik ochilmasa, iltimos, tugmani yana bir bor bosing.
    """
    await message.answer(text, reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())