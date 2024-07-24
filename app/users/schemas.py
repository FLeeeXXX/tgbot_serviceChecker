from pydantic import BaseModel


class SUser(BaseModel):
    id: int
    telegram_id: int

    class Config:
        orm_mode: True
