from aiogram.filters import CommandStart
from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from common.bot_keyboards import start_keyboard, all_products_keyboard
from aiogram.fsm.context import FSMContext
from states.user_states import AddSite, AddProxy
from users.service import UserService
from proxies.service import ProxyService
from sites.service import SiteService
from common.common import bot, start_scheduler

user_handlers = Router()


@user_handlers.message(CommandStart())
async def start(message: types.Message):
    telegram_id = message.from_user.id
    chat_id = str(message.chat.id)

    user = await UserService.find_one_or_none(telegram_id=telegram_id)
    if not user:
        await UserService.add(telegram_id=message.from_user.id)
    await message.answer("Привет!\nТеперь тебе нужно добавить ссылки и прокси", reply_markup=start_keyboard)

    await start_scheduler(telegram_id, chat_id)


@user_handlers.message(F.text.lower().contains('список прокси'))
async def get_proxies(message: types.Message):
    keyboard = await all_products_keyboard(ProxyService, message.from_user.id, "proxy")
    await message.answer("Список Ваших proxy:", reply_markup=keyboard)


@user_handlers.callback_query(F.data.startswith('delete_product_proxy_'))
async def delete_user_site(callback: CallbackQuery):
    product_id = int(callback.data.split('_')[-1])
    result = await ProxyService.delete(product_id)
    await callback.answer(result['message'])

    keyboard = await all_products_keyboard(ProxyService, callback.from_user.id, "proxy")
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@user_handlers.message(F.text.lower().contains('список сайтов'))
async def get_sites(message: types.Message):
    keyboard = await all_products_keyboard(SiteService, message.from_user.id, "site_name")
    await message.answer("Список Ваших сайтов:", reply_markup=keyboard)


@user_handlers.callback_query(F.data.startswith('delete_product_site_name_'))
async def delete_user_site(callback: CallbackQuery):
    product_id = int(callback.data.split('_')[-1])
    result = await SiteService.delete(product_id)
    await callback.answer(result['message'])

    keyboard = await all_products_keyboard(SiteService, callback.from_user.id, "site_name")
    await callback.message.edit_reply_markup(reply_markup=keyboard)


# Добавление прокси
@user_handlers.message(F.text.lower().contains('добавить прокси'))
async def add_proxy(message: types.Message, state: FSMContext):
    await state.set_state(AddProxy.proxy)
    await message.answer("‼️ Вставьте 1 строку с proxy\n‼️ Вид: http://user:pass@ip:port")


@user_handlers.message(AddProxy.proxy)
async def add_proxy_msg(message: types.Message, state: FSMContext):
    await state.update_data(proxy=message.text)
    data = await state.get_data()
    result = await ProxyService.add(telegram_id=message.from_user.id, field_name="proxy", field_data=data["proxy"])
    await message.reply(result['message'])
    await state.clear()


# Добавление сайта
@user_handlers.message(F.text.lower().contains('добавить сайт'))
async def add_site(message: types.Message, state: FSMContext):
    await state.set_state(AddSite.site)
    await message.answer("‼️ Вставьте 1 ссылку на сайт\n‼️ Вид: https://url")


@user_handlers.message(AddSite.site)
async def add_site_msg(message: types.Message, state: FSMContext):
    await state.update_data(site=message.text)
    data = await state.get_data()
    result = await SiteService.add(telegram_id=message.from_user.id, field_name="site_name", field_data=data["site"])
    await message.reply(result['message'])
    await state.clear()
