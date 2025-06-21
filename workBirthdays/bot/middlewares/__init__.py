from aiogram import BaseMiddleware, Router
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME

from .context_data import ContextDataMiddleware
from .context_user import ContextUserMiddleware
from .logging import EventLoggingMiddleware


def setup_middlewares(router: Router):
    base_setup_middleware(router, ContextDataMiddleware(), outer=True)
    base_setup_middleware(router, EventLoggingMiddleware())
    base_setup_middleware(router, ContextUserMiddleware())


def base_setup_middleware(
        router: Router, middleware: BaseMiddleware,
        outer: bool = False
):
    if outer:
        router.message.outer_middleware(middleware)
        router.business_message.outer_middleware(middleware)
        router.callback_query.outer_middleware(middleware)

        update_handler = router.observers.get(DIALOG_EVENT_NAME)
        if update_handler:
            update_handler.outer_middleware(middleware)

    else:
        router.message.middleware(middleware)
        router.business_message.middleware(middleware)
        router.callback_query.middleware(middleware)

        update_handler = router.observers.get(DIALOG_EVENT_NAME)
        if update_handler:
            update_handler.middleware(middleware)
