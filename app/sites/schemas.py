from pydantic import BaseModel


class SSite(BaseModel):
    id: int
    user_telegram_id: int
    proxy: str

    class Config:
        orm_mode: True
