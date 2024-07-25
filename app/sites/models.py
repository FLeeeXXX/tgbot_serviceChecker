from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.users.schemas import SUser


class Site(Base):
    __tablename__ = 'sites'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_telegram_id = mapped_column(ForeignKey('users.telegram_id'), nullable=False)
    site_name: Mapped[str] = mapped_column(String, nullable=False)

    # user: Mapped[SUser] = relationship('User', back_populates='sites')