from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Site(Base):
    __tablename__ = 'sites'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id'), nullable=False)
    site_name: Mapped[str] = mapped_column(String, nullable=False)
    last_status: Mapped[int] = mapped_column(Integer, nullable=False, default=200)
