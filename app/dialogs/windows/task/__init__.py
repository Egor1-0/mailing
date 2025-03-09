from .common import task_menu
from .inviting import select_account_to_invite_window, select_source_to_invite_window, get_links_from_invite_window, \
    get_link_to_invite_window
from .parcing import parcing_window, get_links_window
from .sending_chats import select_account_to_sending_chat_window, get_text_to_sending_chat_window, \
    get_links_to_sending_chat_window
from .sending_ls import select_account_to_sending_ls_window, get_text_to_sending_ls_window, \
    get_links_to_sending_ls_window

task_window = [task_menu,  # common

               parcing_window, get_links_window,  # parcing

               select_account_to_invite_window, select_source_to_invite_window,  # inviting
               get_links_from_invite_window, get_link_to_invite_window,  # inviting

               select_account_to_sending_ls_window, get_text_to_sending_ls_window, # sending ls
               get_links_to_sending_ls_window, # sending ls

               select_account_to_sending_chat_window, get_text_to_sending_chat_window, # sending chat
               get_links_to_sending_chat_window # sending chat
               ]
