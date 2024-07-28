from aiogram import Bot
from app.config import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.mechanisms.mechanisms import check_sites

bot = Bot(token=settings.TOKEN)
scheduler = AsyncIOScheduler()


async def start_scheduler(telegram_id, chat_id):
    async def notify_user():
        result = await check_sites(telegram_id)
        if result:
            await bot.send_message(chat_id, result)

    if not scheduler.running:
        scheduler.add_job(notify_user, 'interval', seconds=30)
        scheduler.start()
