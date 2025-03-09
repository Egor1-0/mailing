from aiogram_dialog import Dialog

from .windows import account_windows, common_windows, task_window

account_dialog = Dialog(*account_windows)
main_dialog = Dialog(*common_windows)
task_dialog = Dialog(*task_window)