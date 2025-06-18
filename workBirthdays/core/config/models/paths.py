from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Paths:
    app_dir: Path

    @property
    def config_path(self) -> Path:
        return self.app_dir / "config"

    @property
    def config_file(self) -> Path:
        return self.config_path / "config.yml"

    @property
    def logging_config_file(self) -> Path:
        return self.config_path / "logging.yml"

    @property
    def log_path(self) -> Path:
        return self.app_dir / "log"

    @property
    def version_path(self) -> Path:
        return self.app_dir / "version.yaml"

    @property
    def src_path(self) -> Path:
        return self.app_dir / "workBirthdays"

    @property
    def media_path(self) -> Path:
        return self.app_dir / "media"

    @property
    def temp_folder_path(self) -> Path:
        return self.app_dir / "temp"

    @property
    def cookies_folder_path(self) -> Path:
        return self.app_dir / "cookies"

    @property
    def core_path(self) -> Path:
        return self.src_path / "core"

    @property
    def bot_path(self) -> Path:
        return self.src_path / "bot"

    @property
    def api_path(self) -> Path:
        return self.src_path / "api"

    @property
    def admin_path(self) -> Path:
        return self.src_path / "flaskadmin"

    @property
    def faststream_path(self) -> Path:
        return self.src_path / "mq"
