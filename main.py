from aiogram import types, executor, Dispatcher, Bot
from config import token

TOKEN = token
bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Привет Антон')


executor.start_polling(dp)