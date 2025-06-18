from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import final

from .app import AppConfig
from .auth import SecurityConfig
from .db import DBConfig
from .paths import Paths
from .redis import RedisConfig
from .web import WebConfig


@dataclass
class BaseConfig:
    app: AppConfig
    paths: Paths
    db: DBConfig
    redis: RedisConfig
    web: WebConfig
    auth: SecurityConfig

    @property
    def app_dir(self) -> Path:
        return self.paths.app_dir

    @property
    def config_path(self) -> Path:
        return self.paths.config_path

    @property
    def log_path(self) -> Path:
        return self.paths.log_path

    @property
    def upload_file_path(self) -> Path:
        return self.paths.media_path

    @final
    def as_base(self):
        return BaseConfig(
            app=self.app, paths=self.paths, db=self.db, redis=self.redis,
            web=self.web, auth=self.auth,
        )
