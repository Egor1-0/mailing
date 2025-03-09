from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel, Multiselect, ScrollingGroup, Column

from dialogs.getters.account_getters import get_accounts
from states import Accounts

from dialogs.callbacks.account_callbacks import delete_accounts

delete_accounts_window = Window(
    Case(texts={
        False: Const('У вас нет аккаунтов'),
        True: Const('Выберите аккаунты, которые нужно удалить'),
    },
        selector='accounts_exits'
    ),
    ScrollingGroup(
        Multiselect(
            Format("✓ {item.phone_number}"),
            Format("{item.phone_number}"),
            id="del_accs",
            item_id_getter=lambda item: item.id,
            items="accounts",
            when='accounts_exits'
        ),
        when='scroll', # ОТОБРАЖАЕТСЯ, КОГДА ОБЪЕКТОВ БОЛЬШЕ 7
        height=7,
        width=1,
        id="group_accs_to_del",

    ),
    Column(
        Multiselect(
            Format("✓ {item.phone_number}"),
            Format("{item.phone_number}"),
            id="del_accs",
            item_id_getter=lambda item: item.id,
            items="accounts",
            when='accounts_exits',
        ),
        when='list' # ОТОБРАЖАЕТСЯ, КОГДА ОБЪЕКТОВ ОТ 1 ДО 7
    ),

    Cancel(
        text=Const('Удалить'),
        id='del_bitton',
        on_click=delete_accounts,
        when='accounts_exits'
    ),
    SwitchTo(text=Const('Назад'),
             id='back',
             state=Accounts.main_acc_menu),
    getter=get_accounts,
    state=Accounts.delete_account
)
