import logging

from telethon import TelegramClient


async def parce_users_from_chats(client: TelegramClient, links: list[str]) -> set | None:
    """используется при задаче парсинг"""
    user_data = set()
    for link in links:
        try:
            chat = await client.get_entity(link)
            participants = await client.get_participants(chat)
            non_admins = [p for p in participants if p.status != 'admin']
            for p in non_admins:
                user_data.add(p)
        except Exception as e:
            logging.warning(f"Ошибка при парсе юзеров в чате: %s, %s", link, e)
    return user_data