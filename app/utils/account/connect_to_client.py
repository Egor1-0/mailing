import logging
import os

from opentele.api import API
from telethon import TelegramClient


def get_session(session_name: str) -> TelegramClient:
    """Создаёт клиента сессии с указанным именем."""
    session_path = os.path.join('sessions', session_name + '.session')
    return TelegramClient(
        session_path,
        API.TelegramDesktop.Generate(unique_id=session_name)
    )