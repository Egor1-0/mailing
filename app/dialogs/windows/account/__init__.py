from aiogram_dialog import Dialog

from .add_accounts import add_account_window, get_code_window, succesful_add_account_window
from .common import account_window, user_accounts_window
from .delete_accounts import delete_accounts_window
from .update_windows import update_account_window

account_windows = [account_window, user_accounts_window, update_account_window,
                   add_account_window, get_code_window,
                   succesful_add_account_window, delete_accounts_window]
