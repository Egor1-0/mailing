import logging

from telethon import TelegramClient


async def parce_from_chats(client: TelegramClient, links: list[str]) -> set | None:
    """используется при задаче парсинг"""
    user_data = set()
    async with client:
        for link in links:
            try:
                chat = await client.get_entity(link)
                participants = await client.get_participants(chat)
                non_admins = [p for p in participants if p.status != 'admin']
                for p in non_admins:
                    user_data.add(f"@{p.username}, ID: {p.id}" if p.username else f"ID: {p.id}")
                async for msg in client.iter_messages(chat): # now only last
                    if msg.from_user:
                        user_data.add(f"@{msg.from_user.username}, ID: {msg.from_user.id}" if msg.from_user.username else f"ID: {msg.from_user.id}")
            except Exception as e:
                logging.error(f"Ошибка при парсе юзеров в чатах: %s, %s", link, e)
    return user_data