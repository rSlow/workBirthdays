from typing import Any

from adaptix import Retort

from workBirthdays.core.config.parser.redis import load_redis_config
from ..models.storage import StorageConfig, StorageType


def load_storage_config(
        dct: dict[str, Any], retort: Retort
) -> StorageConfig:
    storage_type = dct["bot"]["storage"]["type"]
    config = StorageConfig(type_=StorageType[storage_type])
    if config.type_ == StorageType.redis:
        config.redis = load_redis_config(dct["redis"], retort)
    return config
