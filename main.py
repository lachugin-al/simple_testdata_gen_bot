from aiogram import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from create_bot import dp

# Клавиатура бота
b1 = KeyboardButton('/Сгенерировать_карту')
b2 = KeyboardButton('/Тестовые_CVV')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)  # one_time_keyboard=True - прячем клавиатуру
kb_client.add(b1).insert(b2)


async def on_startup(_):
    print('On-air')

# импортируем handlers
from handlers import client, admin, other

client.register_handlers_client(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
