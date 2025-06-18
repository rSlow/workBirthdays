import base64
import logging
from datetime import datetime

import jwt
from passlib.context import CryptContext

from workBirthdays.core.config.models.auth import SecurityConfig
from workBirthdays.core.utils.dates import tz_utc

logger = logging.getLogger(__name__)


class SecurityProps:
    def __init__(self, config: SecurityConfig) -> None:
        super().__init__()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = config.secret_key
        self.algorythm = config.algorythm
        self.access_token_expire = config.token_expire
        self.encoding = config.encoding

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_bearer_token(self, data: dict) -> str:
        data_to_encode = data.copy()
        expire = datetime.now(tz=tz_utc) + self.access_token_expire
        data_to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(data_to_encode, self.secret_key, algorithm=self.algorythm)
        return f"bearer {encoded_jwt}"

    def create_basic_auth(self, tg_id: int, hashed_password: str) -> str:
        creds = f"{tg_id}:{hashed_password}".encode(self.encoding)
        basic = base64.b64encode(creds).decode(self.encoding)
        return f"basic {basic}"

    def decode_basic_auth(self, basic: str) -> tuple[int, str] | None:
        decoded = base64.urlsafe_b64decode(basic).decode(self.encoding)
        tg_id, hashed_password = decoded.split(":", maxsplit=1)
        return int(tg_id), hashed_password
