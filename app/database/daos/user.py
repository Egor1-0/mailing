import logging

from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User, Account
from ..tools import get_session


class UserDAO:
    @staticmethod
    @get_session
    async def add_user(session: AsyncSession, tg_id: int) -> None:
        query_to_get_user = (select(User)
                             .where(User.tg_id == tg_id))
        user = await session.execute(query_to_get_user)
        scalar_user = user.scalar()
        if scalar_user:
            return
        query = (insert(User)
                 .values(tg_id=tg_id))
        await session.execute(query)
        await session.commit()

    @staticmethod
    @get_session
    async def get_user(session: AsyncSession, tg_id: int) -> User | None:
        try:
            query = (select(User)
                     .where(User.tg_id == tg_id)
                     .options(selectinload(User.accounts))) # загрузка аккаунта, если он где то будет использоваться
            result = await session.execute(query)
            return result.scalar()
        except Exception as e:
            logging.error(f'Error while add user {e}')
            await session.rollback()
