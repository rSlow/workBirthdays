from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, validates
from sqlalchemy_utils import URLType

from workBirthdays.core.db import dto
from workBirthdays.core.db.models import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint('user_id', 'url', name='_telegram_id_url_uc'),
    )

    url: Mapped[str] = mapped_column(URLType(), nullable=False)
    name: Mapped[str]
    user_id: Mapped[int]
    frequency: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)

    def to_dto(self):
        return dto.Subscription(
            id_=self.id,
            url=self.url,
            name=self.name,
            user_id=self.user_id,
            frequency=self.frequency,
            is_active=self.is_active,
        )

    @validates("frequency")
    def validate_frequency(self, _: str, frequency: int):
        if frequency < 30:
            raise ValueError("frequency must be greater or equal 30 seconds")
        return frequency
