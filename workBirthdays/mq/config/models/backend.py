from dataclasses import dataclass

from workBirthdays.core.config.models import RedisConfig


@dataclass
class ResultBackendConfig(RedisConfig):
    pass
