import binascii

from dishka import Provider, provide, Scope, from_context
from fastapi import HTTPException, Request, status
from jwt import PyJWTError

from workBirthdays.api.utils.auth import AuthService
from workBirthdays.api.utils.auth.cookie import OAuth2PasswordBearerWithCookie
from workBirthdays.api.utils.exceptions import AuthError
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao import UserDao


class AuthProvider(Provider):
    scope = Scope.APP

    auth_service = provide(AuthService)

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide
    def get_cookie_auth(self) -> OAuth2PasswordBearerWithCookie:
        return OAuth2PasswordBearerWithCookie(token_url="auth/token")

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self,
            request: Request,
            cookie_auth: OAuth2PasswordBearerWithCookie,
            auth_service: AuthService,
            dao: UserDao,
    ) -> dto.User:
        try:
            token = await cookie_auth.get_token(request)
            return await auth_service.get_user_from_bearer(token, dao)
        except (PyJWTError, AuthError, HTTPException):
            try:
                return await auth_service.get_user_from_basic(request, dao)
            except (binascii.Error, AuthError, ValueError):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
