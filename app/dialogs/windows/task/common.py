from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Start, Cancel

from dialogs.callbacks.input_callbacks import correct_name, uncorrect_name, correct_links_to_parce, uncorrect_links
from dialogs.filters import check_spaces, check_links
# from dialogs.callbacks.task_callbacks import get_file
from states import Tasks

task_menu = Window(
    # главное меню
    Const('Выберите задачу'),
    SwitchTo(Const('Рассылка по лс'),
             id='send_to_ls',
             state=Tasks.select_account_to_sending_ls
             ),
    SwitchTo(Const('Рассылка по чатам'),
             id='send_to_chats',
             state=Tasks.select_account_to_sending_chat
             ),
    SwitchTo(Const('Парсинг'),
             id='parcing',
             state=Tasks.select_account_to_parce
             ),
    SwitchTo(Const('Инвайтинг'),
             id='inviting',
             state=Tasks.select_account_to_invite
             ),
    Cancel(Const('Назад'),
           id='to_main'),
    state=Tasks.menu
)



# sending_ls = Window(
#     Const('Отправьте файл с юзернеймами людей, по которым хотите делать рассылку'),
#     MessageInput(get_file, content_types=[ContentType.DOCUMENT]),
#     SwitchTo(text=Const('Назад'),
#              id='go_back',
#              state=Task.menu),
#     state=Task.sending_ls
# )
