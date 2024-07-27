from pydantic import BaseModel


class SProxy(BaseModel):
    id: int
    user_id: int
    proxy: str

    class Config:
        orm_mode: True
