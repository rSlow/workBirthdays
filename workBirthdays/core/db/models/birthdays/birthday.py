from datetime import date
from uuid import UUID

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from workBirthdays.core.db import dto
from ..base import Base


class Birthday(Base):
    __tablename__ = "birthdays"

    uuid: Mapped[UUID] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    fio: Mapped[str]
    date: Mapped[date]
    post: Mapped[str | None]
    rank: Mapped[str | None]

    def to_dto(self):
        return dto.Birthday(
            fio=self.fio,
            date=self.date,
            uuid=self.uuid,
            post=self.post,
            rank=self.rank
        )
