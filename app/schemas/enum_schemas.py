from enum import Enum


class TaskType(str, Enum):
    sending_ls = 'sending_ls'
    parcing = 'parcing'
    sending_chat = 'sending_chat'
    inviting = 'inviting'