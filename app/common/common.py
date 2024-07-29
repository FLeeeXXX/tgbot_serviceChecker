from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from app.config import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.mechanisms.mechanisms import check_sites

bot = Bot(token=settings.TOKEN)
scheduler = AsyncIOScheduler()


async def start_scheduler(telegram_id, chat_id):
    async def notify_user():
        try:
            result = await check_sites(telegram_id)
            if result:
                await bot.send_message(chat_id, result)
        except TelegramForbiddenError:
            job_id = f"check_sites_{telegram_id}"
            if scheduler.get_job(job_id):
                scheduler.remove_job(job_id)
            return
        except Exception as e:
            return

    job_id = f"check_sites_{telegram_id}"

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(notify_user, 'interval', seconds=30, id=job_id)

    if not scheduler.running:
        scheduler.start()
