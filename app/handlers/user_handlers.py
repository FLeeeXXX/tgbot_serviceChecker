from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F
from common.bot_keyboards import start_keyboard
from aiogram.fsm.context import FSMContext
from states.user_states import AddSite, AddProxy
from users.service import UserService

user_handlers = Router()


@user_handlers.message(CommandStart())
async def start(message: types.Message):
    user = await UserService.find_one_or_none(telegram_id=message.from_user.id)
    if not user:
        await UserService.add(telegram_id=message.from_user.id)
    await message.answer("Привет!", reply_markup=start_keyboard)


@user_handlers.message(F.text.lower().contains('список прокси'))
async def get_proxies(message: types.Message):
    await message.answer("Тут выпадет список прокси")


# Добавление прокси
@user_handlers.message(F.text.lower().contains('добавить прокси'))
async def add_proxy(message: types.Message, state: FSMContext):
    await state.set_state(AddProxy.proxy)
    await message.answer("Вставьте строку с proxy")


@user_handlers.message(AddProxy.proxy)
async def add_proxy_msg(message: types.Message, state: FSMContext):
    await state.update_data(proxy=message.text)
    data = await state.get_data()
    await message.answer(f'Прокси: {data["proxy"]}')
    await state.clear()


# Добавление сайта
@user_handlers.message(F.text.lower().contains('добавить сайт'))
async def add_site(message: types.Message, state: FSMContext):
    await state.set_state(AddSite.site)
    await message.answer("Вставьте ссылку на сайт")


@user_handlers.message(AddSite.site)
async def add_site_msg(message: types.Message, state: FSMContext):
    await state.update_data(site=message.text)
    data = await state.get_data()
    await message.answer(f"Сайт: {data['site']}")
    await state.clear()
