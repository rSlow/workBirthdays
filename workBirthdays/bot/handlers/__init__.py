import logging

from aiogram import Dispatcher, Router

from workBirthdays.bot.filters.private import set_chat_private_filter
from . import commands, birthdays
from . import errors

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, log_chat_id: int):
    handlers_router = Router(name=__name__)
    set_chat_private_filter(handlers_router)

    errors.setup(dp, log_chat_id)

    handlers_router.include_routers(commands.setup())
    handlers_router.include_routers(birthdays.setup())

    dp.include_router(handlers_router)

    logger.debug("handlers configured successfully")
