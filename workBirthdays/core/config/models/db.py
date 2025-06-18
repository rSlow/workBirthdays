from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class DBConfig:
    echo: bool
    type: str | None = None
    sync_connector: str | None = None
    async_connector: str | None = None
    host: str | None = None
    port: int | None = None
    login: str | None = None
    password: str | None = None
    name: str | None = None
    path: str | None = None
    echo: bool = False
    file_storages: list[str] = field(default_factory=list)

    def _get_uri(self, connector: str | None = None):
        if self.type in ("mysql", "postgresql"):
            url = self.type
            if connector:
                url += f"+{connector}"
            url += f"://{self.login}:{self.password}@{self.host}"
            if self.port:
                url += f":{self.port}"
            url += f"/{self.name}"
        elif self.type == "sqlite":
            url = f"{self.type}://{self.path}"
        else:
            raise ValueError("DB_TYPE not mysql, sqlite or postgres")
        return url

    @property
    def sync_uri(self):
        return self._get_uri(connector=self.sync_connector)

    @property
    def async_uri(self):
        return self._get_uri(connector=self.async_connector)
