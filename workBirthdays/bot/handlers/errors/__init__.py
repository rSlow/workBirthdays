from aiogram import Dispatcher

from . import dialogs, base


def setup(dp: Dispatcher, log_chat_id: int):
    dialogs.setup(dp)
    base.setup(dp, log_chat_id)
