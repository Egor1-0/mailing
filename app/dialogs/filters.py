import phonenumbers


def check_phone_number(text: str) -> str:
    """проверяет корректность номера телефона"""
    try:
        number = phonenumbers.parse(text, None)
        if not phonenumbers.is_valid_number(number):
            raise ValueError
        return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
    except Exception as e:
        raise ValueError

def check_spaces(text: str):
    """проверяет колво слов в сообщении"""
    if len(text.strip().split()) != 1:
        raise ValueError
    return text.strip()

def check_links(text: str):
    """проверяет что все ссылки корректные"""
    links = text.split()

    for link in links:
        if not (link.startswith('t.me') or link.startswith('@') or link.startswith('https://t.me')):
            raise ValueError
    return links

def check_link(text: str):
    """проверяет что ссылка корректная"""
    if not (text.startswith('t.me') or text.startswith('@') or text.startswith('https://t.me')):
        raise ValueError
    return text