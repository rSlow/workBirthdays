__all__ = [
    "DaoHolder"
]

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .birthday import BirthdayDao
from .log import EventLogDao
from .role import RoleDao
from .subscription import SubscriptionDao
from .user import UserDao


class DaoHolder:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

        self.user: UserDao = UserDao(self.session)
        self.log: EventLogDao = EventLogDao(self.session)
        self.role: RoleDao = RoleDao(self.session)

        self.birthdays: BirthdayDao = BirthdayDao(self.session)
        self.subscription: SubscriptionDao = SubscriptionDao(self.session)
