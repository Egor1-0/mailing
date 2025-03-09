from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Select

from dialogs.callbacks.input_callbacks import correct_links_to_parce, uncorrect_links, get_links_in_file_to_parcing
from dialogs.callbacks.task_callbacks import select_account_to_parce
from dialogs.filters import check_links
from dialogs.getters.account_getters import get_accounts
from states import Tasks

parcing_window = Window(
    Const('Выберите аккаунт'),
    Select(Format('{item.phone_number}'),
           id='select_acc',
           on_click=select_account_to_parce,
           item_id_getter=lambda item: item.id,
           items='accounts'
           ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.menu),
    getter=get_accounts,
    state=Tasks.select_account_to_parce
)

get_links_window = Window(
    Const('Отправьте ссылки. Можно отправить в формате юзернейма, либо файл'),
    TextInput(id="get_links",
              on_success=correct_links_to_parce,
              on_error=uncorrect_links,
              type_factory=check_links
              ),
    MessageInput(get_links_in_file_to_parcing,
                 content_types=[ContentType.DOCUMENT]
                 ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.menu),
    state=Tasks.get_links
)

