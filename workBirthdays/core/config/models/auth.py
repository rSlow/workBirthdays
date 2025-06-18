from dataclasses import dataclass
from datetime import timedelta
from typing import Literal
from urllib.parse import urlparse


@dataclass
class SecurityConfig:
    secret_key: str
    domain: str
    token_expire: timedelta
    httponly: bool
    secure: bool
    tg_bot_username: str
    tg_bot_token: str
    algorythm: str = "HS256"
    samesite: Literal["lax", "strict", "none"] | None = None
    disable_cors: bool = False
    encoding: str = "utf-8"

    @property
    def host(self):
        url = urlparse(self.domain)
        return url.netloc
