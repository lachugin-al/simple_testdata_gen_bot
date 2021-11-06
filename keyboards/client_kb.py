from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Клавиатура бота
b1 = KeyboardButton('/Сгенерировать_карту')
b2 = KeyboardButton('/Тестовые_CVV')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)  # one_time_keyboard=True - прячем клавиатуру
b3 = KeyboardButton('Поделиться номером', request_contact=True)
b4 = KeyboardButton('Отправить расположение', request_location=True)

# kb_client.add(b1).insert(b2)
kb_client.row(b1, b2).add(b3, b4)