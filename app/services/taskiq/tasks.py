import asyncio
import os.path
import logging

from aiofiles import open
from aiogram import Bot
from aiogram.types import FSInputFile
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest, GetForumTopicsRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputPeerChannel, InputUser

from core import config
from database.daos import AccountDAO
from utils.account.connect_to_client import get_session
from .broker import broker
from utils.parcing.parce_users import parce_users_from_chats

bot = Bot(config.bot.TOKEN.get_secret_value())


@broker.task
async def log_message(message: str):
    """тест работы"""
    logging.info(message)


@broker.task
async def send_messages_to_chats(account_id: int, chat_links: list[str], text: str):
    account = await AccountDAO.get_account_by_id(acc_id=account_id)
    client = get_session(account.phone_number)
    async with client:
        for chat_link in chat_links:
            try:
                chat = await client.get_entity(chat_link)

                if hasattr(chat, 'forum') and chat.forum:
                    topics = await client(GetForumTopicsRequest(chat))
                    for topic in topics.topics:
                        try:
                            await client.send_message(
                                entity=chat,
                                message=text,
                                reply_to=topic.id
                            )
                            await asyncio.sleep(2)
                        except Exception as e:
                            logging.error(f"Ошибка при отправке сообщения в топик {topic.id}: {e}")
                            continue
                else:
                    await client.send_message(chat, text)
                    await asyncio.sleep(2)

            except Exception as e:
                logging.error(f"Ошибка при работе с чатом {chat_link}: {e}")
                continue


@broker.task
async def sending_message(account_id: int, chat_link: str, text: str):
    """не используется. должен быть при рассылке"""
    account = await AccountDAO.get_account_by_id(acc_id=account_id)
    client = get_session(account.phone_number)
    async with client:
        users = await parce_users_from_chats(client, [chat_link])
        if not users:
            logging.warning("Не удалось найти пользователей для рассылки.")
            return

        for user in users:
            try:
                recipient = user.username or InputUser(user.id, user.access_hash)

                await client.send_message(recipient, text)
                await asyncio.sleep(1)

            except FloodWaitError as e:
                await asyncio.sleep(e.seconds + 1)
            except Exception as e:
                logging.error("Ошибка при отправке сообщения пользователю %d, %s:", user.id, e)
                continue


@broker.task
async def invite_users(account_id: int, links_from: list[str], link_to: str):
    account = await AccountDAO.get_account_by_id(acc_id=int(account_id))
    client = get_session(account.phone_number)
    async with client:
        try:
            target_entity = await client.get_entity(link_to)
        except Exception as e:
            logging.error(f"Ошибка при получении целевой сущности: {e}")
            raise

        users = await parce_users_from_chats(client, links_from)
        if not users:
            logging.warning("Не удалось найти пользователей для инвайта.")
            return

        try:
            user_ids = [InputUser(user.id, user.access_hash) for user in users]
            if isinstance(target_entity, InputPeerChannel) or (
                    hasattr(target_entity, 'broadcast') and target_entity.broadcast):
                await client(InviteToChannelRequest(target_entity, user_ids))
            else:
                for user_id in user_ids:
                    try:
                        await client(AddChatUserRequest(chat_id=target_entity.id, user_id=user_id, fwd_limit=0))
                    except Exception as e:
                        logging.error(f"Ошибка при добавлении пользователя в чат: {e}")
                        continue
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 1)
        except Exception as e:
            logging.error(f"Ошибка при выполнении инвайта: {e}")


@broker.task
async def parce_users(account_id: int, links: list[str], user_id: int):
    account = await AccountDAO.get_account_by_id(acc_id=account_id)
    client = get_session(account.phone_number)
    async with client:
        user_data = await parce_users_from_chats(client, links)
        if not user_data:
            async with bot:
                await bot.send_message(user_id, 'Произошла ошибка. Не удалось спарсить данные')
            return
        filename = os.path.join('files', f"{account_id}.txt")
    async with open(filename, "w", encoding="utf-8") as f:
        for user in user_data:
            user_str = ''
            if user.username:
                user_str += user.username
            else:
                user_str += str(user.id)
            await f.write(user + "\n")

    input_file = FSInputFile(filename)
    async with bot:
        await bot.send_document(user_id, input_file)
    os.remove(filename)
