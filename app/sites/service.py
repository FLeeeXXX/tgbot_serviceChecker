from app.service.base import BaseService
from app.sites.models import Site
from app.database import async_session
from sqlalchemy import select, insert
from app.users.models import User


class SiteService(BaseService):
    model = Site

    @classmethod
    async def add(cls, telegram_id, field_name, field_data):
        async with async_session() as session:
            try:
                user_result = await session.execute(
                    select(User).filter_by(telegram_id=telegram_id)
                )
                user = user_result.scalars().first()

                query = insert(cls.model).values(user_id=user.id, **{field_name: field_data})

                await session.execute(query)
                await session.commit()
                return {"status": "success", "message": "✅ Успешно!"}
            except Exception as e:
                await session.rollback()
                return {"status": "error", "message": f"❌ {str(e)}"}