from taskiq import AsyncBroker

from workBirthdays.mq.handlers.error import exc_middleware


def setup(broker: AsyncBroker):
    broker.middlewares.insert(0, exc_middleware)
