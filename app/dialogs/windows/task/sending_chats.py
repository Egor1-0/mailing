from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Select

from dialogs.callbacks.input_callbacks import get_text_for_sending_chat, correct_link_to_sending_chat, uncorrect_links
from dialogs.callbacks.task_callbacks import select_account_to_sending_chat
from dialogs.filters import check_link, check_links
from dialogs.getters.account_getters import get_accounts
from states import Tasks

select_account_to_sending_chat_window = Window(
    Const('Выберите аккаунт'),
    Select(Format('{item.phone_number}'),
           id='select_acc',
           on_click=select_account_to_sending_chat,
           item_id_getter=lambda item: item.id,
           items='accounts'
           ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.menu),
    getter=get_accounts,
    state=Tasks.select_account_to_sending_chat
)

get_text_to_sending_chat_window = Window(
    Const(
        'Отправьте текст для рассылки'),
    TextInput(id="get_text",
              on_success=get_text_for_sending_chat,
              ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.select_account_to_sending_chat),
    state=Tasks.get_text_to_sending_chat
)

get_links_to_sending_chat_window = Window(
    Const('Отправьте ссылку на чат'),
    TextInput(id="get_links",
              on_success=correct_link_to_sending_chat,
              on_error=uncorrect_links,
              type_factory=check_links
              ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.get_text_to_sending_chat),
    state=Tasks.get_users_to_sending_chat
)
