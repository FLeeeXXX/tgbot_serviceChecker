import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from aiohttp import web
from aiogram import Dispatcher
from app.common.common import bot
from app.handlers.user_handlers import user_handlers
from app.config import settings

# Создаем экземпляр Dispatcher
dp = Dispatcher()

# Включаем маршрутизаторы
dp.include_routers(
    user_handlers,
)

# Функция для инициализации вебхука
async def on_startup(app):
    await bot.set_webhook(settings.WH_URL)

# Функция для завершения работы
async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

# Создаем приложение aiohttp
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Добавляем путь для вебхука
app.router.add_post(settings.WH_PATH, dp.webhook_handler)

# Запуск приложения
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8443)
