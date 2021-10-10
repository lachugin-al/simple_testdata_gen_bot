from aiogram import types, Dispatcher
from create_bot import dp, bot  # импортируем уже созданные экземпляры

from cardgen import Card_Generator


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет, я ваш помошник в генерации тестовых данных') # reply_markup=kb_client
        await message.delete()
    except:
        await message.reply('Общение с ботом через личные сообщения, напишити ему: \nhttps://t.me/SimpleTestDataGenbot')


# @dp.message_handler(commands=['Сгенерировать_карту'])
async def gen_card(message: types.Message):
    await message.delete()
    await message.answer('Сгенерировал карту для оплаты в тестинге ' + Card_Generator.generate_pan())


# @dp.message_handler(commands=['Тестовые_CVV'])
async def help(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, """
    Успешная оплата - 123
    На карте недостаточно средств - 129
    Ошибка платежной системы - 208
    Оплата не более 5 рублей - 321
    Оплата только первый платеж - 325
     """)


# записываем команды для передачи хендлеров
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(gen_card, commands=['Сгенерировать_карту'])
    dp.register_message_handler(help, commands=['Тестовые_CVV'])
