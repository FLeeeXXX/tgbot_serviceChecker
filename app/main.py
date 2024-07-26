import asyncio
from aiogram import Dispatcher
from common.common import bot
from handlers.user_handlers import user_handlers

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
