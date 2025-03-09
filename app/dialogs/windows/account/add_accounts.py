from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Cancel, ListGroup, Button

from dialogs.callbacks.input_callbacks import error_phone_handler, correct_phone_handler
from dialogs.filters import check_phone_number
from dialogs.getters.account_getters import get_phone_number, get_numpad, get_current_code
from states import Accounts

from dialogs.callbacks.account_callbacks import update_code

add_account_window = Window(
    Const('Введите номер телефона для добавления аккаунтов, либо нажмите кнопку назад'),
    TextInput(
        id='phone_number_input',
        type_factory=check_phone_number,
        on_error=error_phone_handler,
        on_success=correct_phone_handler
    ),
    SwitchTo(text=Const('Назад'),
             id='back',
             state=Accounts.main_acc_menu),
    state=Accounts.add_account
)

get_code_window = Window(
    Multi(
        Format(text='Введите код, который вам прислал телеграм на номер {user_number}, '
                    'или нажмите назад. Используйте кнопку стереть чтобы стереть'),
        Format(text='Текущий код: {code}'),
        sep='\n\n'
    ),
    Group(
        ListGroup(
            Button(Format('{item}'),
                   id='list_of_butn_to_upd',
                   on_click=update_code),
            id='input_code',
            items='numpad',
            item_id_getter=lambda item: item),
        width=3,
    ),
    SwitchTo(text=Const('Назад'),
             id='back',
             state=Accounts.add_account),
    getter=[get_phone_number, get_numpad, get_current_code],
    state=Accounts.get_code
)

succesful_add_account_window = Window(
    Format(text='Номер {user_number} успешно добавлен!'),
    Cancel(
        text=Const('В меню'),
        id='to_menu'
    ),
    getter=get_phone_number,
    state=Accounts.succesful_add_account
)
