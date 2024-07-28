import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from app.common.common import bot
from app.handlers.user_handlers import user_handlers
from app.config import settings

dp = Dispatcher()
dp.include_router(user_handlers)

async def on_startup(app):
    await bot.set_webhook(settings.WH_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def handle(request):
    update = Update(**await request.json())
    await dp.feed_update(bot, update)
    return web.Response()

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app.router.add_post(settings.WH_PATH, handle)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8443)


