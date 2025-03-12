from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Task
from ..models.tasks import TaskType
from ..tools import get_session


class TaskDAO:
    @staticmethod
    @get_session
    async def add_passed_task(session: AsyncSession, user_id: int, task: TaskType) -> None:
        query = insert(Task).values(user_id=user_id, task=task)
        await session.execute(query)
        await session.commit()
