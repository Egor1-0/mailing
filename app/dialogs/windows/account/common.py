from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Case, List
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Cancel

from dialogs.getters.account_getters import get_accounts
from states import Accounts

account_window = Window(
    Const('Выберите действие'),
    Group(
        SwitchTo(text=Const('Мои аккаунты'),
                 id='my_accs',
                 state=Accounts.my_accounts),
        SwitchTo(text=Const('Изменить аккаунт'),
                 id='update_account',
                 state=Accounts.update_account),
        SwitchTo(text=Const('Добавить аккаунт'),
                 id='add_account',
                 state=Accounts.add_account),
        SwitchTo(text=Const('Удалить аккаунт'),
                 id='del_account',
                 state=Accounts.delete_account),
        Cancel(text=Const('Назад'),
               id='back'),
    ),
    state=Accounts.main_acc_menu
)

user_accounts_window = Window(
    Case(texts={
        False: Const('У вас нет аккаунтов'),
        True: List(field=Format('~ {item.phone_number}'),
                   items='accounts',
                   ),
    },
        selector='accounts_exits'
    ),
    SwitchTo(text=Const('Назад'),
             id='back',
             state=Accounts.main_acc_menu),
    getter=get_accounts,
    state=Accounts.my_accounts
)
