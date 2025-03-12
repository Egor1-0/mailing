from aiogram.types import User

from database.daos import UserDAO


async def get_profile_info(event_from_user: User, **kwargs):
    """здесь должна быть статистика. но ее нет пока что"""
    user_data = await UserDAO.get_statistics(event_from_user.id)
    return {'user_id': event_from_user.id,
            'subscribe': 'Отсутствует',
            'count_accounts': user_data[0],
            'passed_tasks': user_data[1],
            }