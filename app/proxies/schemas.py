from pydantic import BaseModel


class SProxy(BaseModel):
    id: int
    user_telegram_id: int
    site_name: str

    class Config:
        orm_mode: True
