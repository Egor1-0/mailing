import logging

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from states import Tasks


async def select_account_to_parce(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str):
    """сохраняет выбранный аккаунт"""
    dialog_manager.dialog_data['selected_account'] = item_id
    await dialog_manager.switch_to(Tasks.get_links)


async def select_account_to_invite(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str):
    """сохраняет выбранный аккаунт"""
    dialog_manager.dialog_data['selected_account'] = item_id
    await dialog_manager.switch_to(Tasks.select_type_source)


async def select_account_to_sending_ls(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str):
    """сохраняет выбранный аккаунт"""
    dialog_manager.dialog_data['selected_account'] = item_id
    await dialog_manager.switch_to(Tasks.get_text_to_sending_ls)


async def select_account_to_sending_chat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str):
    """сохраняет выбранный аккаунт"""
    dialog_manager.dialog_data['selected_account'] = item_id
    await dialog_manager.switch_to(Tasks.get_text_to_sending_chat)