from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.sites.schemas import SSite
from app.proxies.schemas import SProxy


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)

    sites: Mapped[list[SSite]] = relationship('Site', back_populates='user', cascade='all, delete-orphan')
    proxies: Mapped[list[SProxy]] = relationship('Proxy', back_populates='user', cascade='all, delete-orphan')