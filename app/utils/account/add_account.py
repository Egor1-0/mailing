import os.path

from opentele.tl import TelegramClient
from opentele.api import API
from telethon.errors import PhoneNumberInvalidError, SessionPasswordNeededError, PhoneCodeExpiredError

from .connect_to_client import get_session


async def get_code_phone(phone: str):
    """запрос кода по номеру телефона"""
    client = get_session(phone)
        
    if not client.is_connected():
        await client.connect()
    
    try:
        send_code = await client.send_code_request(phone)
        phone_code_hash = send_code.phone_code_hash
        return phone_code_hash
    except PhoneNumberInvalidError:
       return False
    except PhoneCodeExpiredError:
       return False

        
async def try_to_connect(phone: str, code: int, phone_code_hash: str):
    """попытка подключения по коду, телефону и хэшу"""
    try:
        client = get_session(phone)
        
        if not client.is_connected():
            await client.connect()
            
        await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
        client.session.save()
        return True
    except SessionPasswordNeededError:
        return False
    except Exception as e:
        print(e)
        return False
    