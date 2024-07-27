from pydantic import BaseModel


class SSite(BaseModel):
    id: int
    user_id: int
    site_name: str
    last_status: int

    class Config:
        orm_mode: True
