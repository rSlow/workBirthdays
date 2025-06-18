from sqlalchemy import BigInteger, sql
from sqlalchemy.orm import mapped_column, Mapped, relationship

from workBirthdays.core.db import dto
from workBirthdays.core.db.models import Base
from workBirthdays.core.db.models.mixins.time import TimeMixin
from .roles import Role, UsersRoles


class User(TimeMixin, Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}  # TODO eager_defaults

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None] = mapped_column(nullable=True, unique=True)
    hashed_password: Mapped[str | None]
    is_bot: Mapped[bool] = mapped_column(
        default=False, server_default=sql.false()
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False, server_default=sql.false()
    )
    is_active: Mapped[bool] = mapped_column(
        default=True, server_default=sql.true()
    )
    roles: Mapped[list[Role]] = relationship(
        secondary=UsersRoles, back_populates="users",
    )

    def __repr__(self) -> str:
        rez = (
            f"<User "
            f"id={self.id} "
            f"tg_id={self.tg_id} "
            f"name={self.first_name} {self.last_name} "
        )
        if self.username:
            rez += f"username=@{self.username}"
        return rez + ">"

    def to_dto(self) -> dto.User:
        return dto.User(
            id_=self.id,
            tg_id=self.tg_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            is_bot=self.is_bot,
            is_superuser=self.is_superuser,
            is_active=self.is_active,
            roles=[role.name for role in self.roles],
        )
