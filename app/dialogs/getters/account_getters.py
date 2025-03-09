from aiogram.types import User
from aiogram_dialog import DialogManager

from database.daos import UserDAO


async def get_accounts(dialog_manager: DialogManager, **kwargs):
    """ВОЗВРАЩАЕТ ПАРАМЕТРЫ: accounts_exits: BOOL, СУЩЕСТВУЮТ ЛИ ВООБЩЕ АККАУНТЫ.
    accounts: LIST СПИСОК ВСЕХ АККАУНТОВ ЮЗЕРА
    list: BOOL ВОЗВРАЩАЕ ТРУ ЕСЛИ НУЖНО СДЕЛАТЬ ВЫВОД БЕЗ СКРОЛА
    scroll: BOOL ВОЗВРАЩАЕТ ТРУ ЕСЛИ НУЖНО СДЕЛАТЬ ВЫВОД СО СКРОЛОМ
    """
    user_data = await UserDAO.get_user(dialog_manager.event.from_user.id)
    accs = user_data.accounts
    return {'accounts_exits': bool(accs),
            'accounts': accs,
            'list': 0 < len(accs) <= 7,
            'scroll': 8 <= len(accs),
            }


async def get_phone_number(dialog_manager: DialogManager, **kwargs):
    """ВОЗВРАЩАЕТ НОМЕР, КОТОРЫЙ ВВЕЛ ЮЗЕР"""
    return {'user_number': dialog_manager.dialog_data['user_number']}


# async def get_selected_account(dialog_manager: DialogManager):
#     """ВОЗВРАЩАЕТ АЙДИ АККАУНТА ДЛЯ ИЗМЕНЕНИЯ"""
#     return {'selected_account_id': dialog_manager.dialog_data['selected_account_id']}


async def get_numpad(**kwargs):
    """ВОЗВРАЩАЕТ СПИСОК, КОТОРЫЙ ПРЕВРАЩАЕТСЯ В КЛАВИАТУРУ В ВИДЕ НУМПАДА"""
    return {'numpad': [7, 8, 9, 4, 5, 6, 1, 2, 3, '-', 0, 'enter']}


async def get_current_code(dialog_manager: DialogManager, **kwargs):
    """ВОЗВРАЩАЕТ КОД, КОТОРЫЙ ВВЕЛ ЮЗЕР"""
    return {'code': dialog_manager.dialog_data.get('current_code')}