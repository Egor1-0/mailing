from aiogram.types import User


async def get_profile_info(event_from_user: User, **kwargs):
    """здесь должна быть статистика. но ее нет пока что"""
    # user_data = get_from_db()
    return {'user_id': event_from_user.id,
            'subscribe': 'Отсутствует',
            'count_accounts': 0,
            'count_invites': 0,
            'leaved_comms': 0,
            'passed_tasks': 0,
            }