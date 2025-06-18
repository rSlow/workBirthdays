from datetime import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from workBirthdays.core.db import dto
from ..base import Base


class NotificationState(Base):
    __tablename__ = "birthdays_notification_states"

    user_id: Mapped[int] = mapped_column(unique=True)
    timeshift: Mapped[time] = mapped_column(
        default=lambda: time(hour=0, minute=0)
    )
    times: Mapped[list["NotificationTime"]] = relationship()

    def to_dto(self):
        return dto.NotificationState(
            id_=self.id,
            user_id=self.user_id,
            timeshift=self.timeshift,
        )


class NotificationTime(Base):
    __tablename__ = "birthdays_notification_times"

    time: Mapped[time]
    user_state_id: Mapped[int] = mapped_column(
        ForeignKey("birthdays_notification_states.id", ondelete="CASCADE")
    )

    def to_dto(self):
        return dto.NotificationTime(
            id_=self.id,
            time=self.time,
        )
