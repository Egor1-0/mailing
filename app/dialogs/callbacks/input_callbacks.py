import logging

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from dialogs.filters import check_links
from states import Accounts, Tasks
from utils.account.add_account import get_code_phone, try_to_connect
from services.taskiq.tasks import parce_users, invite_users


async def error_phone_handler(message: Message,
                              widget: ManagedTextInput,
                              dialog_manager: DialogManager,
                              error: ValueError):
    await message.answer('Некорректный номер телефона')


async def correct_phone_handler(message: Message,
                                widget: ManagedTextInput,
                                dialog_manager: DialogManager,
                                text: str):
    hash = await get_code_phone(text)
    if not hash:
        await message.answer('Произошла ошибка. Введите другой номер')
        return
    dialog_manager.dialog_data['user_number_hash'] = hash
    dialog_manager.dialog_data['user_number'] = text
    dialog_manager.dialog_data['current_code'] = ''
    await dialog_manager.switch_to(Accounts.get_code)


async def correct_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['base_name'] = text
    await dialog_manager.switch_to(Tasks.get_links)


async def uncorrect_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error: ValueError):
    await message.answer('Название должно быть одним словом. Для удобства можно написать вот так: тестовое_название')


async def correct_links_to_parce(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager,
                                 data: list[str]):
    account_id = int(dialog_manager.dialog_data['selected_account'])
    await parce_users.kiq(account_id=account_id, links=data,
                          user_id=dialog_manager.event.from_user.id)
    await dialog_manager.done()


async def correct_links_from_invite(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager,
                                    data: list[str]):
    dialog_manager.dialog_data['links'] = data
    await dialog_manager.switch_to(Tasks.get_link_to_invite)


async def correct_link_to_invite(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, data: str):
    links = dialog_manager.dialog_data['links']
    acc = dialog_manager.dialog_data['selected_account']
    await invite_users.kiq(acc, links, data)
    await dialog_manager.done()


async def uncorrect_links(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error: ValueError):
    await message.answer('Отправьте валидные данные. Примеры: t.me/yourchat или @yourchat')


async def get_links_in_file(message: Message,
                            message_input: MessageInput,
                            dialog_manager: DialogManager):
    if message.document.file_name[-4:] != '.txt':
        await message.answer('Отправьте .txt файл')
        return

    file_id = message.document.file_id
    file = await message.bot.download(file_id)
    try:
        links = check_links(file.read().decode('utf-8'))
    except ValueError:
        await message.answer('Ссылки некорректны')
        return

    dialog_manager.dialog_data['links'] = links
    await dialog_manager.switch_to(Tasks.get_link_to_invite)


async def get_links_in_file_to_parcing(message: Message,
                                       message_input: MessageInput,
                                       dialog_manager: DialogManager):
    if message.document.file_name[-4:] != '.txt':
        await message.answer('Отправьте .txt файл')
        return

    file_id = message.document.file_id
    file = await message.bot.download(file_id)
    try:
        links = check_links(file.read().decode('utf-8'))
    except ValueError:
        await message.answer('Ссылки некорректны')
        return

    account_id = int(dialog_manager.dialog_data['selected_account'])
    await parce_users.kiq(account_id=account_id, links=links,
                          user_id=dialog_manager.event.from_user.id)
    await dialog_manager.done()


async def get_text_for_sending_ls(message: Message,
                                  message_input: MessageInput,
                                  dialog_manager: DialogManager,
                                  data: dict):
    dialog_manager.dialog_data['text_to_sending'] = data
    await dialog_manager.switch_to(Tasks.get_users_to_sending_ls)


async def correct_link_to_sending_ls(message: Message,
                                     widget: ManagedTextInput,
                                     dialog_manager: DialogManager,
                                     data: dict):
    text = dialog_manager.dialog_data['text_to_sending']
    acc = dialog_manager.dialog_data['selected_account']
    ...  # await invite_users.kiq(acc, links, data)
    await dialog_manager.done()


async def get_text_for_sending_chat(message: Message,
                                  message_input: MessageInput,
                                  dialog_manager: DialogManager,
                                  data: dict):
    dialog_manager.dialog_data['text_to_sending'] = data
    await dialog_manager.switch_to(Tasks.get_users_to_sending_chat)


async def correct_link_to_sending_chat(message: Message,
                                     widget: ManagedTextInput,
                                     dialog_manager: DialogManager,
                                     data: dict):
    text = dialog_manager.dialog_data['text_to_sending']
    acc = dialog_manager.dialog_data['selected_account']
    ...  # await invite_users.kiq(acc, links, data)
    await dialog_manager.done()
