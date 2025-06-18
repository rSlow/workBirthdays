from dishka import Scope, provide, Provider, provide_all

from workBirthdays.core.db.dao import DaoHolder
from workBirthdays.core.db.dao.birthday import BirthdayDao
from workBirthdays.core.db.dao.log import EventLogDao
from workBirthdays.core.db.dao.notification import UserNotificationDao
from workBirthdays.core.db.dao.role import RoleDao
from workBirthdays.core.db.dao.subscription import SubscriptionDao
from workBirthdays.core.db.dao.user import UserDao


class DaoProvider(Provider):
    scope = Scope.REQUEST

    holder = provide(DaoHolder)

    dao = provide_all(
        UserDao,
        EventLogDao,
        BirthdayDao,
        UserNotificationDao,
        RoleDao,
        SubscriptionDao
    )
