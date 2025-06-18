from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from workBirthdays.core.db import dto
from workBirthdays.core.db.models import Base

UsersRoles = Table(
    "users_roles",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "role_id",
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    ),
)


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True)
    alias: Mapped[str]
    users = relationship(
        "User", secondary=UsersRoles,
        back_populates="roles", uselist=True,
    )

    def to_dto(self):
        return dto.UserRole(
            id_=self.id,
            name=self.name,
            alias=self.alias,
        )
