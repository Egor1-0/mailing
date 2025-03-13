from aiogram.fsm.state import State, StatesGroup

class MainWindow(StatesGroup):
    start = State()
    profile = State()
    accounts = State()
    subscribe = State()


class Accounts(StatesGroup):
    main_acc_menu = State()
    my_accounts = State()

    add_account = State()
    get_code = State()
    succesful_add_account = State()

    delete_account = State()

    update_account = State()
    update_events = State()


class Tasks(StatesGroup):
    menu = State()

    # parcing
    select_account_to_parce = State()
    get_links = State()

    #inviting
    select_account_to_invite = State()
    select_type_source = State()
    get_links_from_invite = State()
    get_link_to_invite = State()
    select_base = State()

    # sending ls
    select_account_to_sending_ls = State()
    get_text_to_sending_ls = State()
    get_users_to_sending_ls = State()

    # sending chat
    select_account_to_sending_chat = State()
    get_text_to_sending_chat = State()
    get_users_to_sending_chat = State()

