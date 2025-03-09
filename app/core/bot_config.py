from pydantic import SecretStr

from .base_config import BaseConfig


class BotConfig(BaseConfig):
    TOKEN: SecretStr