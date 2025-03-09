from .base_config import BaseConfig


class RedisConfig(BaseConfig):
    REDIS_HOST: str
    REDIS_PORT: int