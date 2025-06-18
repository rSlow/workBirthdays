from aiogram import Dispatcher, BaseMiddleware
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME

from .context_data import ContextDataMiddleware
from .logging import EventLoggingMiddleware


def setup_middlewares(dp: Dispatcher):
    _base_setup_middleware(dp, ContextDataMiddleware(), outer=True)
    _base_setup_middleware(dp, EventLoggingMiddleware())


def _base_setup_middleware(
        dp: Dispatcher, middleware: BaseMiddleware,
        outer: bool = False
):
    if outer:
        dp.message.outer_middleware(middleware)
        dp.business_message.outer_middleware(middleware)
        dp.callback_query.outer_middleware(middleware)

        update_handler = dp.observers[DIALOG_EVENT_NAME]
        update_handler.outer_middleware(middleware)

    else:
        dp.message.middleware(middleware)
        dp.business_message.middleware(middleware)
        dp.callback_query.middleware(middleware)

        update_handler = dp.observers[DIALOG_EVENT_NAME]
        update_handler.middleware(middleware)
