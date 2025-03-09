from pydantic import SecretStr
from sqlalchemy import URL

from .base_config import BaseConfig


class DatabaseConfig(BaseConfig):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_USER: str
    POSTGRES_DB: str

    def create_url(self):
        """создает и возвращает юрл для подключения к бд через алхимию"""
        # return 'sqlite+aiosqlite:///data/test.db'
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            database=self.POSTGRES_DB,
        )