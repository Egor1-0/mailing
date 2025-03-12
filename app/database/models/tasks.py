from enum import Enum

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class TaskType(str, Enum):
    sending_ls = 'sending_ls'
    parcing = 'parcing'
    sending_chat = 'sending_chat'
    inviting = 'inviting'


class Task(Base):
    __tablename__ = 'tasks'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    task: Mapped[TaskType]

    user: Mapped['User'] = relationship(
        back_populates='accounts'
    )