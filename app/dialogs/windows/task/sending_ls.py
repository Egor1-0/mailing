from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Select, Row

from dialogs.callbacks.input_callbacks import (uncorrect_links, get_links_in_file,
                                               correct_links_from_invite, correct_link_to_invite,
                                               get_text_for_sending_ls, correct_link_to_sending_ls)
from dialogs.callbacks.task_callbacks import select_account_to_invite, select_account_to_sending_ls
from dialogs.filters import check_links, check_link
from dialogs.getters.account_getters import get_accounts
from states import Tasks

select_account_to_sending_ls_window = Window(
    Const('Выберите аккаунт'),
    Select(Format('{item.phone_number}'),
           id='select_acc',
           on_click=select_account_to_sending_ls,
           item_id_getter=lambda item: item.id,
           items='accounts'
           ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.menu),
    getter=get_accounts,
    state=Tasks.select_account_to_sending_ls
)

get_text_to_sending_ls_window = Window(
    Const(
        'Отправьте текст для рассылки'),
    TextInput(id="get_text",
              on_success=get_text_for_sending_ls,
              ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.select_account_to_sending_ls),
    state=Tasks.get_text_to_sending_ls
)

get_links_to_sending_ls_window = Window(
    Const('Отправьте ссылку на чат, из которого нужно брать людей для рассылки'),
    TextInput(id="get_links",
              on_success=correct_link_to_sending_ls,
              on_error=uncorrect_links,
              type_factory=check_link
              ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.get_text_to_sending_ls),
    state=Tasks.get_users_to_sending_ls
)
