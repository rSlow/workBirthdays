from adaptix import Retort

from ..models.redis import RedisConfig


def load_redis_config(redis_dict: dict, retort: Retort) -> RedisConfig:
    return retort.load(redis_dict, RedisConfig)
