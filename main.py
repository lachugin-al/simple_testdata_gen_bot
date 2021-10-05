from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import json, string, random

bot = Bot(token='2055868218:AAGsPuMjLoaqE9uh8V_pNgTX5BM2FxccoYc')
dp = Dispatcher(bot)

# Генератор карт
# decimal_decoder = lambda s: int(s, 10)
# decimal_encoder = lambda i: str(i)
decimal_decoder = None
decimal_encoder = None
new_card = None

class Card_Generator(object):
    @staticmethod
    def luhn_sum_mod_base(s):
        digits = [int(c) for c in s]
        b = 10
        return (sum(digits[::-2]) +
                sum(sum(divmod(2 * d, b)) for d in digits[-2::-2])) % b

    @staticmethod
    def verify(s):
        return Card_Generator.luhn_sum_mod_base(s) == 0

    @staticmethod
    def generate(s):
        d = Card_Generator.luhn_sum_mod_base(s + '0')
        if d != 0:
            d = 10 - d
        return str(d)

    @staticmethod
    def generate_pan(pan_len=16):
        prefix = '510000'
        base = prefix + str(random.randint(
            10 ** (pan_len - len(prefix) - 2),
            10 ** (pan_len - len(prefix) - 1) - 1))
        pan = base + Card_Generator.generate(base)
        assert Card_Generator.verify(pan)
        return pan


def start_generator():
    global decimal_decoder
    global decimal_encoder
    global new_card
    decimal_decoder = lambda s: int(s, 10)
    decimal_encoder = lambda i: str(i)
    new_card = Card_Generator.generate_pan()
    return new_card


# new_card = start_generator()

# Клавиатура бота
b1 = KeyboardButton('/Сгенерировать_карту')
b2 = KeyboardButton('/Тестовые_CVV')
#
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)  # one_time_keyboard=True - прячем клавиатуру
kb_client.add(b1).insert(b2)


async def on_startup(_):
    print('On-air')


# Клиентская часть
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет, я ваш помошник в генерации тестовых данных',
                               reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через личные сообщения, напишити ему: \nhttps://t.me/SimpleTestDataGenbot')


@dp.message_handler(commands=['Сгенерировать_карту'])
async def gen_card(message: types.Message):
    start_generator()
    await message.delete()
    await message.answer('Сгенерировал карту для оплаты в тестинге ' + new_card)


@dp.message_handler(commands=['Тестовые_CVV'])
async def help(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, """
    Успешная оплата - 123
    На карте недостаточно средств - 129
    Ошибка платежной системы - 208
    Оплата не более 5 рублей - 321
    Оплата только первый платеж - 325
     """)


# ----------------------------------------
# test
@dp.message_handler()
async def echo_send(message: types.Message):
    if message.text.lower() == 'test':
        await message.answer('passed')


# Проверка на матерные и запрещенные слова
@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('censure.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()


executor.start_polling(dp, on_startup=on_startup)
