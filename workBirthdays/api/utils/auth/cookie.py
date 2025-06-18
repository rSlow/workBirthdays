from typing import Optional

from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.responses import Response

from workBirthdays.core.config.models.auth import SecurityConfig
from workBirthdays.core.utils.auth.token import Token


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            token_url: str,
            scheme_name: Optional[str] = None,
            auto_error: bool = True
    ):
        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=token_url))
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    @staticmethod
    async def get_token(request: Request) -> Token:
        authorization = request.cookies.get("Authorization", "")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return Token(value=param, type_="bearer")

    __call__ = get_token


def set_auth_cookie(config: SecurityConfig, response: Response, token: Token):
    response.set_cookie(
        "Authorization",
        value=f"{token.type_} {token.value}",
        samesite=config.samesite,
        domain=config.host,
        httponly=config.httponly,
        secure=config.secure,
        max_age=config.token_expire.seconds,
    )
