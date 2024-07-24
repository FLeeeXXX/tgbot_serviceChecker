from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class SingletonDatabaseMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonDatabaseMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonDatabaseMeta):
    def __init__(self, db_url='sqlite+aiosqlite:///database.sqlite3'):
        self.engine = create_async_engine(db_url)
        self.async_session = async_sessionmaker(self.engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


db = Database()
async_session = db.async_session
