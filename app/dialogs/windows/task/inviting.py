from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Select, Row

from dialogs.callbacks.input_callbacks import (uncorrect_links, get_links_in_file,
                                               correct_links_from_invite, correct_link_to_invite)
from dialogs.callbacks.task_callbacks import select_account_to_invite
from dialogs.filters import check_links, check_link
from dialogs.getters.account_getters import get_accounts
from states import Tasks

select_account_to_invite_window = Window(
    Const('Выберите аккаунт'),
    Select(Format('{item.phone_number}'),
           id='select_acc',
           on_click=select_account_to_invite,
           item_id_getter=lambda item: item.id,
           items='accounts'
           ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.menu),
    getter=get_accounts,
    state=Tasks.select_account_to_invite
)

select_source_to_invite_window = Window(
    Const('Выберите откуда приглашать юзеров'),
    Row(
        SwitchTo(text=Const('База'),
                 id='base',
                 state=Tasks.select_base),
        SwitchTo(text=Const('Ссылки'),
                 id='url',
                 state=Tasks.get_links_from_invite),
    ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.select_account_to_invite),
    state=Tasks.select_type_source
)

get_links_from_invite_window = Window(
    Const(
        'Отправьте ссылки, откуда приглашать юзеров. Можно отправить в формате юзернейма или ссылки. Сообщением либо файлом'),
    TextInput(id="get_links",
              on_success=correct_links_from_invite,
              on_error=uncorrect_links,
              type_factory=check_links
              ),
    MessageInput(get_links_in_file,  # не работает
                 content_types=[ContentType.DOCUMENT]
                 ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.select_type_source),
    state=Tasks.get_links_from_invite
)

get_link_to_invite_window = Window(
    Const('Отправьте ссылку, куда надо пригласить. Можно отправить в формате юзернейма или ссылки'),
    TextInput(id="get_links",
              on_success=correct_link_to_invite,
              on_error=uncorrect_links,
              type_factory=check_link
              ),
    SwitchTo(text=Const('Назад'),
             id='go_back',
             state=Tasks.get_links_from_invite),
    state=Tasks.get_link_to_invite
)
