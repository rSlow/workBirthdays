import logging
import typing as t
from functools import wraps

import jwt
from dishka import AsyncContainer
from dishka.integrations.fastapi import inject
from fastapi import HTTPException, Request
from sqlalchemy.exc import NoResultFound
from starlette import status

from workBirthdays.api.utils.exceptions import (
    EmptyPayloadError, InvalidJWTError, AuthHeaderMissingError,
    UnknownSchemaError
)
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao import UserDao
from workBirthdays.core.utils.auth.security import SecurityProps
from workBirthdays.core.utils.auth.token import Token
from workBirthdays.core.utils.exceptions.user import UnknownUsernameFound, UnknownUserIdError

logger = logging.getLogger(__name__)
T = t.TypeVar("T")
P = t.ParamSpec("P")


def auth_required(func: t.Callable[P, T]) -> t.Callable[P, T]:
    @inject
    @wraps(func)
    async def decorated(*args, **kwargs):
        for kwarg in kwargs.values():
            if isinstance(kwarg, Request):
                dishka: AsyncContainer = kwarg.state.dishka_container
                if dishka is not None:
                    user = await dishka.get(dto.User)
                    if user is not None:
                        return await func(*args, **kwargs)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return decorated


class AuthService:
    def __init__(self, security: SecurityProps) -> None:
        self.security = security

    async def authenticate_user(self, tg_id: int, password: str, user_dao: UserDao) -> dto.User:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect TG ID or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            user = await user_dao.get_by_tg_id_with_password(tg_id)
        except UnknownUsernameFound as e:
            raise http_status_401 from e

        password_hash = user.hashed_password or ""
        if not self.security.verify_password(password, password_hash):
            raise http_status_401

        return user.without_password()

    async def update_user_password(self, user: dto.User, password: str, user_dao: UserDao) -> None:
        hashed_password = self.security.get_password_hash(password)
        await user_dao.set_password(user, hashed_password)

    def create_user_jwt_token(self, user: dto.User) -> str:
        return self.security.create_bearer_token(data={"sub": str(user.id_)})

    def create_user_basic_token(self, user: dto.UserWithCreds) -> str:
        return self.security.create_basic_auth(
            tg_id=user.tg_id, hashed_password=user.hashed_password
        )

    async def get_user_from_bearer(self, token: Token, user_dao: UserDao) -> dto.User:
        logger.debug("try to check token %s", token)
        try:
            payload: dict = jwt.decode(
                token.value,
                key=self.security.secret_key,
                algorithms=[self.security.algorythm],
            )
            if payload.get("sub") is None:
                logger.warning("valid jwt contains no user id")
                raise EmptyPayloadError
            user_db_id = int(t.cast(str, payload.get("sub")))

        except jwt.PyJWTError as e:
            logger.info("invalid jwt", exc_info=e)
            raise InvalidJWTError

        except Exception as e:
            logger.warning("some jwt error", exc_info=e)
            raise e

        try:
            user = await user_dao.get_by_id(user_db_id)
        except NoResultFound:
            logger.info("user by id %s not found", user_db_id)
            raise UnknownUserIdError(user_id=user_db_id)

        return user

    async def get_user_from_basic(self, request: Request, user_dao: UserDao) -> dto.User:
        if (header := request.headers.get("Authorization")) is None:
            raise AuthHeaderMissingError
        schema, token = header.split(" ", maxsplit=1)
        if schema.lower() != "basic":
            raise UnknownSchemaError(schema=schema)
        tg_id, _ = self.security.decode_basic_auth(token)
        return await user_dao.get_by_tg_id_with_password(tg_id)
