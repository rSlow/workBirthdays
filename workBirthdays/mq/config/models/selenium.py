from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class SeleniumDriverType(StrEnum):
    REMOTE = "remote"
    CHROME = "chrome"


@dataclass
class SeleniumProxy:
    scheme: str
    host: str
    port: int | None = None
    username: str | None = None
    password: str | None = None

    @property
    def uri(self):
        res = f"{self.scheme}://"
        if self.username and self.password:
            res += f"{self.username}:{self.password}@"
        res += self.host
        if self.port:
            res += f":{self.port}"
        return res


@dataclass
class SeleniumConfig:
    type_: SeleniumDriverType
    host: str | None = None
    port: int | None = None
    path: Path | str | None = None
    proxy: SeleniumProxy | None = None

    @property
    def uri(self):
        res = "http://" + self.host
        if self.port is not None:
            res += f":{self.port}"
        return res + "/wd/hub"
