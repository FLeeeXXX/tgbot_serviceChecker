import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import Update
from app.common.common import bot
from app.handlers.user_handlers import user_handlers
from app.config import settings



WEBHOOK_PATH = "/webhook"
WEB_SERVER_PORT = 3000
WEB_SERVER_HOST = "https://tgbot-servicechecker.onrender.com"
WEB_SERVER_URL = f"{WEB_SERVER_HOST}{WEBHOOK_PATH}"


async def on_startup(bot: Bot):
    await bot.set_webhook(WEB_SERVER_URL)


async def on_shutdown(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)


async def main():
    dp = Dispatcher()

    dp.include_routers(
        user_handlers,
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == '__main__':
    asyncio.run(main())