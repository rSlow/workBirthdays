from typing import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis

from workBirthdays.core.config.models import BaseConfig
from workBirthdays.core.config.models.redis import RedisConfig
from workBirthdays.core.factory.redis import create_redis


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    def get_redis_config(self, base_config: BaseConfig) -> RedisConfig:
        return base_config.redis

    @provide
    async def get_redis(
            self, redis_config: RedisConfig
    ) -> AsyncIterable[Redis]:
        async with create_redis(redis_config) as redis:
            yield redis
