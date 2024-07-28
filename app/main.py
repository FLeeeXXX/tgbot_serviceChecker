import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from aiogram import Dispatcher
from app.common.common import bot
from app.handlers.user_handlers import user_handlers


dp = Dispatcher()

dp.include_routers(
    user_handlers,
)


# webhook вместо start_polling юзается только на проде
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_my_commands(commands=, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
