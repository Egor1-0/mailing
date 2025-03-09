from pydantic import BaseModel

from .bot_config import BotConfig
from .database_config import DatabaseConfig
from .redis_config import RedisConfig


class AppConfig(BaseModel):
    bot: BotConfig = BotConfig()
    database: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()

config = AppConfig()
