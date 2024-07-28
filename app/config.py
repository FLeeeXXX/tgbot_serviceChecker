from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    WEBHOOK_PATH: str
    WEB_SERVER_PORT: int
    WEB_SERVER_HOST: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def WEB_SERVER_URL(self):
        return f"https://tgbot-servicechecker.onrender.com{self.WEBHOOK_PATH}"

    class Config:
        env_file = '.env'


settings = Settings()
