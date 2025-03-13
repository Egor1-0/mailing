from enum import Enum

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from schemas.enum_schemas import TaskType


class Task(Base):
    __tablename__ = 'tasks'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    task: Mapped[TaskType]

    user: Mapped['User'] = relationship(
        back_populates='tasks'
    )