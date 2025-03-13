from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Start

from dialogs.getters.main_dialog_getters import get_profile_info
from states import MainWindow, Accounts, Tasks

main_menu = Window(
    # главное меню
    Const('Добро пожаловать!'),
    Group(
        SwitchTo(text=Const('Профиль'),
                 id='profile_button',
                 state=MainWindow.profile),
        Start(text=Const('Аккаунты'),
              id='account_button',
              state=Accounts.main_acc_menu),
        Start(text=Const('Новая задача'),
              id='new_task',
              state=Tasks.menu),
    ),
    state=MainWindow.start
)
profile_window = Window(
    # профиль, где будет статистика
    Multi(
        Const('- Общая информация:'),
        Format('Айди пользователя <code>{user_id}</code>\n'),
        Const('- Статистика за все время:'),
        Format('Загружено аккаунтов в бота: <code>{count_accounts}</code> шт'),
        Format('Выполнено задач: <code>{passed_tasks}</code> шт'),
        sep='\n'
    ),
    SwitchTo(text=Const('Подписка'),
             id='subscribe',
             state=MainWindow.subscribe),
    SwitchTo(text=Const('Назад'),
             id='bask',
             state=MainWindow.start),
    getter=get_profile_info,
    state=MainWindow.profile
)
