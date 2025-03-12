from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    accounts: Mapped[list['Account']] = relationship(
        back_populates='user'
    )
    tasks: Mapped[list['Task']] = relationship(
        back_populates='user'
    )