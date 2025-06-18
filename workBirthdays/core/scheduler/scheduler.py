import logging
from asyncio import Protocol

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer
from redis import Redis

from workBirthdays.core.config.models.redis import RedisConfig
from workBirthdays.core.db import dto
from workBirthdays.core.scheduler.context import SchedulerInjectContext
from workBirthdays.core.utils.dates import tz_local

logger = logging.getLogger(__name__)


class Scheduler(Protocol):
    async def start(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def __aenter__(self):
        logger.info("Starting scheduler")
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class ApScheduler(Scheduler):
    def __init__(self, dishka: AsyncContainer, redis_config: RedisConfig):
        SchedulerInjectContext.container = dishka
        self.job_store = RedisJobStore(
            host=redis_config.host,
            port=redis_config.port,
            db=redis_config.db,
            password=redis_config.password
        )
        self.job_store.redis = Redis.from_url(redis_config.uri)
        self.executor = AsyncIOExecutor()
        job_defaults = {  # TODO check
            "coalesce": False,
            "max_instances": 20,
            "misfire_grace_time": 3600,
        }
        logger.info("configuring shedulder...")
        self.scheduler = AsyncIOScheduler(
            jobstores={"default": self.job_store},
            job_defaults=job_defaults,
            executors={"default": self.executor},
            timezone=tz_local
        )

    async def start(self):
        self.scheduler.start()

    async def close(self):
        self.scheduler.shutdown()
        self.executor.shutdown()
        self.job_store.shutdown()

    # ----- TASKS ----- #

    # ----- BIRTHDAYS ----- #
    def add_birthday_notification(
            self, notification: dto.NotificationTime, state: dto.NotificationState
    ):

        self.scheduler.add_job(
            func="workBirthdays.core.scheduler.task_wrappers.birthdays:"
                 "check_birthdays",
            id=_prepare_notification_key(notification.id_),
            trigger="cron",
            hour=(notification.time.hour + state.timeshift.hour) % 24,
            minute=(notification.time.minute + state.timeshift.minute) % 60,
            kwargs={"user_id": state.user_id}
        )

    def remove_birthday_notification(self, notification_id: int):
        job_id = _prepare_notification_key(notification_id)
        try:
            self.scheduler.remove_job(job_id=job_id)
        except JobLookupError as e:
            logger.error(
                "can't remove job %s for birthday notification %s",
                job_id,
                notification_id,
                exc_info=e,
            )

    def update_user_birthdays(
            self, state: dto.NotificationState,
            notifications: list[dto.NotificationTime]
    ):
        for notification in notifications:
            self.remove_birthday_notification(notification.id_)
            self.add_birthday_notification(notification, state)

    # ----- SUBSCRIPTIONS ----- #
    def add_ad_subscription(self, subscription: dto.Subscription):
        self.scheduler.add_job(
            func="workBirthdays.core.scheduler.task_wrappers.subs:"
                 "check_subscription",
            id=_prepare_subscription_key(subscription.id_),
            trigger="interval",
            seconds=subscription.frequency,
            kwargs={"subscription_id": subscription.id_}
        )

    def remove_ad_subscription(self, subscription_id: int):
        job_id = _prepare_subscription_key(subscription_id)
        try:
            self.scheduler.remove_job(job_id=job_id)
        except JobLookupError as e:
            logger.error(
                "can't remove job %s for ad subscription %s",
                job_id,
                subscription_id,
                exc_info=e,
            )

    def update_user_ad_subscriptions(self, *subscriptions: dto.Subscription):
        for subscription in subscriptions:
            if subscription.is_active:
                self.remove_ad_subscription(subscription.id_)
                self.add_ad_subscription(subscription)


def _prepare_notification_key(notification_id: int) -> str:
    return f"notification-{notification_id}"


def _prepare_subscription_key(subscription_id: int) -> str:
    return f"subscription-{subscription_id}"
