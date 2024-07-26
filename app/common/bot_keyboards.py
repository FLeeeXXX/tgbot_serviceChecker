from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Список прокси"), KeyboardButton(text="Список сайтов")],
    [KeyboardButton(text="Добавить прокси"), KeyboardButton(text="Добавить сайт")],
], resize_keyboard=True)


async def all_products_keyboard(model, telegram_id, field_name):
    products = await model.find_user_data(telegram_id)
    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.add(InlineKeyboardButton(text=getattr(product, field_name), callback_data=f"product_{field_name}_{product.id}"))
        keyboard.add(InlineKeyboardButton(text="❌", callback_data=f"delete_product_{field_name}_{product.id}"))

    return keyboard.adjust(2).as_markup()
