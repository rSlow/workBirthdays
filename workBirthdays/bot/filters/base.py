from aiogram import F, Router
from aiogram.dispatcher.event.handler import CallbackType
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME

F_MD = F["middleware_data"]


def set_filter_on_router(router: Router, filter_: CallbackType):
    router.message.filter(filter_)
    router.business_message.filter(filter_)
    router.callback_query.filter(filter_)
    update_handler = router.observers.get(DIALOG_EVENT_NAME)
    if update_handler is not None:
        update_handler.filter(filter_)
