from __future__ import annotations

from dataclasses import dataclass, field

from aiogram import types as tg


@dataclass
class User:
    id_: int | None = None
    tg_id: int | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_bot: bool | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None
    roles: list[str] = field(default_factory=list)

    @property
    def fullname(self) -> str:
        if self.first_name is None:
            return ""
        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def name_mention(self) -> str:
        return (
                self.fullname
                or self.username
                or str(self.tg_id)
                or str(self.id_)
                or "unknown"
        )

    @property
    def short_mention(self) -> str:
        return (
                self.first_name
                or self.username
                or self.name_mention
        )

    @classmethod
    def from_aiogram(cls, user: tg.User) -> User:
        return cls(
            tg_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_bot=user.is_bot,
            is_active=True
        )

    def with_password(self, hashed_password: str) -> UserWithCreds:
        return UserWithCreds(
            id_=self.id_, tg_id=self.tg_id, username=self.username,
            first_name=self.first_name, last_name=self.last_name,
            is_bot=self.is_bot, is_superuser=self.is_superuser,
            is_active=self.is_active, roles=self.roles,
            hashed_password=hashed_password
        )


@dataclass
class UserWithCreds(User):
    hashed_password: str | None = None

    def without_password(self) -> User:
        return User(
            id_=self.id_, tg_id=self.tg_id, username=self.username,
            first_name=self.first_name, last_name=self.last_name,
            is_bot=self.is_bot, is_superuser=self.is_superuser,
            is_active=self.is_active, roles=self.roles,
        )


@dataclass
class UserRole:
    name: str
    alias: str
    id_: int | None = None

    @property
    def mention(self):
        return f"{self.alias} ({self.name})"
