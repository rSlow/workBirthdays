from dataclasses import dataclass

from workBirthdays.core.config import BaseConfig
from .backend import ResultBackendConfig


@dataclass
class TaskiqAppConfig(BaseConfig):
    result_backend: ResultBackendConfig | None = None

    @classmethod
    def from_base(
            cls, base: BaseConfig,
            result_backend: ResultBackendConfig | None = None,
    ):
        return TaskiqAppConfig(
            app=base.app, paths=base.paths, db=base.db, redis=base.redis, web=base.web, mq=base.mq,
            auth=base.auth,
            result_backend=result_backend,
        )
