import logging

from redis.asyncio import Redis

from workBirthdays.core.config.models.redis import RedisConfig

logger = logging.getLogger(__name__)


def create_redis(config: RedisConfig) -> Redis:
    logger.info("created redis with url %s", config.uri)
    return Redis.from_url(config.uri)
