import logging
from datetime import timedelta

from dishka import FromDishka

from workBirthdays.core.db.dao.subscription import SubscriptionDao
from workBirthdays.core.db.dao.user import UserDao
from workBirthdays.core.scheduler.context import SchedulerInjectContext
from workBirthdays.core.utils.dates import get_now
from workBirthdays.mq.tasks.subs import check_ads

logger = logging.getLogger(__name__)


@SchedulerInjectContext.inject
async def check_subscription(
        subscription_id: int,
        subs_dao: FromDishka[SubscriptionDao],
        user_dao: FromDishka[UserDao],
):
    sub = await subs_dao.get(subscription_id)
    user = await user_dao.get_by_id(sub.user_id)

    check_time = get_now() - timedelta(seconds=sub.frequency)
    check_timestamp = int(check_time.timestamp())
    request_url = str(sub.url) + f"&date_created_min={check_timestamp}"
    await check_ads.kiq(url=request_url, user_id=user.id_, sub_id=sub.id_)
