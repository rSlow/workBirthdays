import logging

from dishka import Provider, Scope, from_context
from taskiq import TaskiqMessage

from workBirthdays.mq.config.models.main import TaskiqAppConfig

logger = logging.getLogger(__name__)


class TaskiqProvider(Provider):
    scope = Scope.APP

    event = from_context(TaskiqMessage, scope=Scope.REQUEST)
    config = from_context(TaskiqAppConfig)
