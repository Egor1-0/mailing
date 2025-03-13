import asyncio
import logging
import os.path
from pathlib import Path

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.enums.parse_mode import ParseMode
from aiogram_dialog import setup_dialogs
from redis.asyncio.client import Redis

from services.taskiq.scheduler import nats_source
from services.taskiq.broker import broker
from services.taskiq.tasks import log_message
from database.tools import create_tables_if_not_exist, drop_tables
from dialogs import main_dialog, account_dialog, task_dialog
from handlers.start import start_router
from core import config


async def main():
    # await drop_tables()
    await create_tables_if_not_exist()

    await nats_source.startup()
    await broker.startup()
    await log_message.kiq('taskiq test')  # тест, что таскик работает

    redis = Redis(
        host=config.redis.REDIS_HOST,
        port=config.redis.REDIS_PORT
    )
    storage = RedisStorage(redis=redis,
                           key_builder=DefaultKeyBuilder(with_destiny=True))
    logging.info(await redis.ping())  # тест, что редис запустился и работает

    bot = Bot(token=config.bot.TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    dp.include_routers(start_router, main_dialog, account_dialog, task_dialog)

    await bot.delete_webhook(drop_pending_updates=True)

    setup_dialogs(dp)  # настройка диалогов
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        filename=os.path.join(Path(__file__).resolve().parent.parent, 'logs', 'logs.log'), filemode='a')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
