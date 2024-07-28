import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import Update
from app.common.common import bot
from app.handlers.user_handlers import user_handlers
from app.config import settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_PATH = "/webhook"
WEB_SERVER_PORT = 3000
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_URL = f"https://tgbot-servicechecker.onrender.com{WEBHOOK_PATH}"


async def on_startup(bot: Bot):
    logger.info(f"Setting webhook to {WEB_SERVER_URL}")
    webhook_set = await bot.set_webhook(WEB_SERVER_URL)
    if webhook_set:
        logger.info("Webhook set successfully")
    else:
        logger.error("Failed to set webhook")


async def on_shutdown(bot: Bot):
    logger.info("Deleting webhook")
    webhook_deleted = await bot.delete_webhook(drop_pending_updates=True)
    if webhook_deleted:
        logger.info("Webhook deleted successfully")
    else:
        logger.error("Failed to delete webhook")


async def create_app():
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

    return app


def main():
    try:
        app = asyncio.run(create_app())
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if not app['client_session'].closed:
            asyncio.run(app['client_session'].close())


if __name__ == '__main__':
    main()
