from datetime import datetime

from sqlalchemy import DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from workBirthdays.core.db import dto
from workBirthdays.core.db.models import Base


class LogEvent(Base):
    __tablename__ = "log_events"

    event_type: Mapped[str]
    chat_id: Mapped[int] = mapped_column(BigInteger)
    dt: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    content_type: Mapped[str | None]
    data: Mapped[str | None]

    def to_dto(self) -> dto.LogEvent:
        return dto.LogEvent(
            type_=self.event_type,
            chat_id=self.chat_id,
            dt=self.dt,
            user_id=self.user_id,
            content_type=self.content_type,
            data=self.data,
        )
