import logging

from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User, Account
from ..tools import get_session


class AccountDAO:
    @staticmethod
    @get_session
    async def add_account(session: AsyncSession, phone_number: str, tg_id: int) -> None:
        try:
            query_to_get_user = (select(User)
                        .where(User.tg_id == tg_id))
            user = await session.execute(query_to_get_user)
            scalar_user = user.scalar()
            query = (insert(Account)
                     .values(phone_number=phone_number, user_id=scalar_user.id))
            await session.execute(query)
            await session.commit()
        except Exception as e:
            logging.error(f'Error while add account {e}')
            await session.rollback()

    @staticmethod
    @get_session
    async def delete_account(session: AsyncSession, acc_id: int) -> None:
        query = (delete(Account)
                 .where(Account.id == acc_id))
        await session.execute(query)
        await session.commit()

    @staticmethod
    @get_session
    async def get_account_by_id(session: AsyncSession, acc_id: int) -> Account:
        query = (select(Account)
                 .where(Account.id == acc_id))
        result = await session.execute(query)
        return result.scalar()

