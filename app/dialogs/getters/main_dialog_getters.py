from aiogram.types import User

from database.daos import UserDAO

from schemas.schemas import Statistics


async def get_profile_info(event_from_user: User, **kwargs):
    """Получение данных для профиля"""
    user_data: Statistics = await UserDAO.get_statistics(event_from_user.id)
    return {'user_id': event_from_user.id,
            'subscribe': 'Отсутствует',
            'count_accounts': user_data.count_accounts,
            'passed_tasks': user_data.count_tasks,
            }