import os

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from database.daos import AccountDAO
from states import Accounts
from utils.account.add_account import try_to_connect


async def select_acc_to_update(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """СОХРАНЯЕТ АЙДИ АККАУНТА, КОТОРЫЙ БУДЕТ ОБНОВЛЕН"""
    dialog_manager.dialog_data['selected_account_id'] = dialog_manager.item_id
    await dialog_manager.switch_to(Accounts.update_events)


async def delete_accounts(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """ДОСТАЕТ ИЗ ДАТЫ АККАУНТЫ, КОТОРЫЕ НЕОБХОДИМО УДАЛИТЬ И УДАЛЯЕТ"""
    data = dialog_manager.find('del_accs').get_checked() or []
    items = [await AccountDAO.get_account_by_id(int(i)) for i in data]
    for item in items:
        try:
            await AccountDAO.delete_account(acc_id=int(item.id))
            os.remove(os.path.join('sessions', item.phone_number + '.session'))
        except:
            pass
    await callback.answer('Аккаунты удалены')


async def update_code(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """ЕСЛИ ЗНАК МИНУС - УБИРАЕТ ОДИН СИМВОЛ КОДА. ЕСЛИ ЦИФРА - ДОПИСЫВАЕТ В КОНЕЦ.
    ЕСЛИ ЭНТЕР - ПРОБУЕТ ПОДКЛЮЧИТЬСЯ И В СЛУЧАЕ УСПЕХА СОХРАНЯЕТ ДАННЫЕ"""
    item = dialog_manager.item_id
    match item:
        case '-':
            dialog_manager.dialog_data['current_code'] = dialog_manager.dialog_data['current_code'][:-1]
        case 'enter':
            phone_code_hash = dialog_manager.dialog_data['user_number_hash']
            phone = dialog_manager.dialog_data['user_number']
            code = int(dialog_manager.dialog_data['current_code'])
            conn = await try_to_connect(phone=phone, code=code, phone_code_hash=phone_code_hash)
            tg_id = dialog_manager.event.from_user.id
            await AccountDAO.add_account(phone_number=phone, tg_id=tg_id)
            if conn:
                await dialog_manager.switch_to(Accounts.succesful_add_account)
            else:
                await callback.answer('Произошла ошибка. Введите код заново')
                dialog_manager.dialog_data['current_code'] = ''
            return
        case _:
            dialog_manager.dialog_data['current_code'] = dialog_manager.dialog_data['current_code'] + item
