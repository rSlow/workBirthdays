from .config import BaseConfigProvider
from .dao import DaoProvider
from .db import DbProvider
from .lock import LockProvider
from .redis import RedisProvider
from .scheduler import SchedulerProvider
from .security import SecurityProvider
from ..config import BaseConfig


def get_common_sync_providers(app_config: BaseConfig):
    return [
        BaseConfigProvider(app_config),
        SecurityProvider(),
    ]


def get_common_providers(app_config: BaseConfig):
    return [
        *get_common_sync_providers(app_config),
        DbProvider(),
        DaoProvider(),
        RedisProvider(),
        LockProvider(),
        SchedulerProvider(),
    ]
