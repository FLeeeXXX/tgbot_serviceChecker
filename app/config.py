from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    WH_HOST: str
    WA_PORT: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def WH_URL(self):
        return f"{self.WH_HOST}{self.WH_PATH}"

    @property
    def WH_PATH(self):
        return f"/webhook/{self.TOKEN}"

    class Config:
        env_file = '.env'


settings = Settings()
