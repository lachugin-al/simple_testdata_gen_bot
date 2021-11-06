# машина состояний
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Проверяем является ли пользователь администратором/модератором группы
# Получаем ID текущего пользователя
# Сообщение /moderator необходимо отправлять в группу!!!
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def admin_make_changes(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что пожелаете?')
    await message.delete()
    # await bot.delete_message()


# Начало диалога загрузхки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None) # коментируем так как ниже мы добавили отдельно хэндлеры
async def cm_start(message: types.Message):
    if message.from_user.id == ID:  # добавляем проверки на каждую команду, админ ли это или нет
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

    # await FSMAdmin.photo.set()
    # await message.reply('Загрузи фото')


# Начинаем ловить ответы и записываем их в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id  # по каждой картинке будет свой уникальный id
    await FSMAdmin.next()
    await message.reply('Введите название')


# Ловим ответ на 'Введите название'
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите описание')


# Ловим ответ на 'Введите описание'
# @dp.message_handler(state=FSMAdmin.name)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Укажите цену')


# Ловим ответ на 'Укажите цену'
# @dp.message_handler(state=FSMAdmin.name)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    async with state.proxy() as data:
        await message.reply(str(data))  # выводим что записал пользователь, либо записываем в базу данных
    await state.finish()  # бот выходит из машины состояний


# Выходим из машины состоний
# @dp.message_handler(state='*', commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


# записываем команды для передачи хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(admin_make_changes, commands=['moderator'], is_chat_admin=True)
