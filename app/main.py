import asyncio
from aiogram import Bot, Dispatcher, types
from config import settings
from handlers.user_handlers import user_handlers


# webhook вместо start_polling юзается только на проде
async def main():
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        user_handlers,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_my_commands(commands=, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        raise KeyboardInterrupt
