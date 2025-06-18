from typing import AsyncIterable

from dishka import Provider, Scope, provide, AsyncContainer

from workBirthdays.core.config.models.redis import RedisConfig
from workBirthdays.core.scheduler.scheduler import ApScheduler


class SchedulerProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_scheduler(
            self, dishka: AsyncContainer, redis_config: RedisConfig
    ) -> AsyncIterable[ApScheduler]:
        async with ApScheduler(
                dishka=dishka,
                redis_config=redis_config
        ) as scheduler:
            yield scheduler
