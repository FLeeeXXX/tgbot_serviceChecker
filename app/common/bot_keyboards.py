from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Список прокси"), KeyboardButton(text="Список сайтов")],
    [KeyboardButton(text="Добавить прокси"), KeyboardButton(text="Добавить сайт")],
], resize_keyboard=True)
