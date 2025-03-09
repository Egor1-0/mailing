import asyncio
import os.path
import logging

from aiofiles import open
from aiogram import Bot
from aiogram.types import FSInputFile
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputPeerChannel, InputPeerChat, InputUser

from core import config
from database.daos import AccountDAO
from utils.account.connect_to_client import get_session
from utils.parcing.parce_users import parce_from_chats
from .broker import broker

bot = Bot(config.bot.TOKEN.get_secret_value())


# не дружу я с юзерботами, а тут именно он и нужен, поэтому пока не доделал (((


@broker.task
async def log_message(message: str):
    """тест работы"""
    logging.info(message)


@broker.task
async def sending_message(phone_number: str, chat_link: str, text: str):
    """не используется. должен быть при рассылке"""
    try:
        client: TelegramClient = get_session(phone_number)
        await client.connect()
        await client.send_message(chat_link, text)
    except Exception as e:
        logging.info('error to connect session with number: %s with error %s', phone_number, e)


@broker.task
async def parce_users(account_id: int, links: list[str], user_id: int):
    account = await AccountDAO.get_account_by_id(acc_id=account_id)
    client = get_session(account.phone_number)
    user_data = await parce_from_chats(client, links)
    if not user_data:
        async with bot:
            await bot.send_message(user_id, 'Произошла ошибка. Не удалось спарсить данные')
        return
    filename = os.path.join('files', f"{account_id}.txt")
    async with open(filename, "w", encoding="utf-8") as f:
        for user in user_data:
            await f.write(user + "\n")

    input_file = FSInputFile(filename)
    async with bot:
        await bot.send_document(user_id, input_file)

    os.remove(filename)


@broker.task
async def invite_users(account_id, links_from: list[str], link_to: str):
    """ХУЙ ЕГО ЗНАЕТ КАК НО РАБОТАЕТ"""
    account = await AccountDAO.get_account_by_id(acc_id=int(account_id))
    client = get_session(account.phone_number)
    await client.connect()
    try:
        target_entity = await client.get_entity(link_to)
    except Exception as e:
        raise e

    for link_from in links_from:
        try:
            chat = await client.get_entity(link_from)

            if isinstance(chat, InputPeerChannel) or hasattr(chat, 'broadcast') and chat.broadcast:
                participants = await client.get_participants(chat)
                user_ids = [p.id for p in participants if p.username]
                if isinstance(target_entity, InputPeerChannel) or (
                        hasattr(target_entity, 'broadcast') and target_entity.broadcast):
                    await client(InviteToChannelRequest(target_entity, user_ids))
                else:
                    for user_id in user_ids:
                        try:
                            await client(AddChatUserRequest(chat_id=target_entity.id, user_id=user_id, fwd_limit=0))
                        except Exception:
                            continue

            elif isinstance(chat, InputPeerChat) or (hasattr(chat, 'megagroup') and chat.megagroup) or (
                    hasattr(chat, "gigagroup") and chat.gigagroup):
                participants = await client.get_participants(chat)
                user_ids = [InputUser(p.id, p.access_hash) for p in participants if p.username]

                if isinstance(target_entity, InputPeerChannel) or (
                        hasattr(target_entity, 'broadcast') and target_entity.broadcast):
                    await client(InviteToChannelRequest(target_entity, user_ids))
                else:
                    for user_id in user_ids:
                        try:
                            await client(AddChatUserRequest(chat_id=target_entity.id, user_id=user_id, fwd_limit=0))
                        except Exception:
                            continue
            else:
                participants = await client.get_participants(chat)
                user_ids = [InputUser(p.id, p.access_hash) for p in participants if p.username]
                if isinstance(target_entity, InputPeerChannel) or (
                        hasattr(target_entity, 'broadcast') and target_entity.broadcast):
                    await client(InviteToChannelRequest(target_entity, user_ids))
                else:
                    for user_id in user_ids:
                        try:
                            await client(AddChatUserRequest(chat_id=target_entity.id, user_id=user_id, fwd_limit=0))
                        except Exception:
                            continue
        except Exception as e:
            logging.error('Ошибка при инвайтинге %s', e)
        await asyncio.sleep(5)
