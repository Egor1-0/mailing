from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.kbd import SwitchTo, ListGroup, Button, ScrollingGroup

from dialogs.getters.account_getters import get_accounts
from states import Accounts

from dialogs.callbacks.account_callbacks import select_acc_to_update

update_account_window = Window(
    Case(texts={
        False: Const('У вас нет аккаунтов'),
        True: Format('Выберите аккаунт, который хотите изменить')
    },
        selector='accounts_exits'
    ),
    ScrollingGroup(
        ListGroup(
            Button(Format('{item[1]}'),
                   id='list_of_butn_to_upd',
                   on_click=select_acc_to_update),
            id='select_account',
            items='accounts',
            item_id_getter=lambda item: item[0],
        ),
        height=7,
        width=1,
        id='group_of_butn_to_upd',
        when='accounts_exits'
    ),
    SwitchTo(text=Const('Назад'),
             id='back',
             state=Accounts.main_acc_menu),
    getter=get_accounts,
    state=Accounts.update_account,
)
