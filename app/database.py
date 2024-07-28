from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


class DatabaseMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DatabaseMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):
    def __init__(self, db_url=settings.DATABASE_URL):
        self.engine = create_async_engine(db_url)
        self.async_session = async_sessionmaker(self.engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


db = Database()
async_session = db.async_session
