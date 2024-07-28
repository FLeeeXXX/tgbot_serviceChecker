import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from app.common.common import bot
from app.handlers.user_handlers import user_handlers
from app.config import settings


async def main():
    dp = Dispatcher()
    dp.include_router(user_handlers)

    try:
        await dp.start_polling(bot, allowed_updates=Update.ANY)
    finally:
        await dp.storage.close()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
