import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from database.daos import UserDAO
from services.taskiq.tasks import log_message
from states import MainWindow

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await UserDAO.add_user(tg_id=message.from_user.id)
    await dialog_manager.start(state=MainWindow.start, mode=StartMode.RESET_STACK)