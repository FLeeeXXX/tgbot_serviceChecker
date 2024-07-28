from app.database import async_session
from sqlalchemy import select, insert, delete, update
from app.users.models import User


class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session() as session:
            query = select(cls.model).filter_by(telegram_id=model_id)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def find_user_data(cls, telegram_id):
        async with async_session() as session:
            user_result = await session.execute(
                select(User).filter_by(telegram_id=telegram_id)
            )
            user = user_result.scalars().first()

            query = select(cls.model).filter_by(user_id=user.id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def delete(cls, product_id):
        async with async_session() as session:
            try:
                query = delete(cls.model).where(cls.model.id == product_id)

                await session.execute(query)
                await session.commit()
                return {"status": "success", "message": "✅ Успешно!"}
            except Exception as e:
                await session.rollback()
                return {"status": "error", "message": f"❌ {str(e)}"}

    @classmethod
    async def change_by_id(cls, model_id, **data):
        async with async_session() as session:
            query = update(cls.model).filter_by(id=model_id).values(**data)
            await session.execute(query)
            await session.commit()
