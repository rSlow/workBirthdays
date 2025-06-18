import logging
import random
from typing import cast

from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent, NoContextError, OutdatedIntent
from dishka import AsyncContainer

from workBirthdays.bot.states.start import MainMenuSG
from workBirthdays.bot.views.alert import BotAlert

logger = logging.getLogger(__name__)


async def clear_unknown_intent(error: types.ErrorEvent, bot: Bot):
    assert error.update.callback_query
    assert error.update.callback_query.message
    logger.warning(f"Unknown intent: {str(error.exception)}")

    try:
        await bot.edit_message_reply_markup(
            chat_id=error.update.callback_query.message.chat.id,
            message_id=error.update.callback_query.message.message_id,
            reply_markup=None
        )
    except TelegramBadRequest:
        pass


async def no_context(
        error: types.ErrorEvent, bot: Bot, dialog_manager: DialogManager
):
    logger.error("No dialog context found", exc_info=error.exception)
    message = error.update.message or error.update.callback_query.message
    assert message
    if message:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Произошла ошибка бота, мы вынуждены вернуть вас "
                 f"в главное меню, и уже работаем над устранением 🛠"
        )
        await dialog_manager.start(
            MainMenuSG.state, mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND
        )


async def outdated_intent(
        error: types.ErrorEvent, bot: Bot, dialog_manager: DialogManager,
        event_chat: types.Chat
):
    exception = cast(OutdatedIntent, error.exception)
    message = error.update.message or error.update.callback_query.message
    logger.warning(f"Outdated intent for stack {exception.stack_id}")

    dialog_message_id: int = dialog_manager.current_stack().last_message_id
    if dialog_message_id != message.message_id:
        message_to_del = random.choice([dialog_message_id, message.message_id])
        dishka: AsyncContainer = dialog_manager.middleware_data["dishka_container"]
        alert = await dishka.get(BotAlert)
        await alert(
            f"outdated intent: {dialog_message_id = }, {message.message_id = }"
            f"deleted message: {message_to_del}"
        )
        try:
            await bot.delete_message(
                chat_id=event_chat.id, message_id=message_to_del
            )
        except TelegramBadRequest:
            pass


def setup(dp: Dispatcher):
    dp.errors.register(
        clear_unknown_intent, ExceptionTypeFilter(UnknownIntent)
    )
    dp.errors.register(
        no_context, ExceptionTypeFilter(NoContextError)
    )
    dp.errors.register(
        outdated_intent, ExceptionTypeFilter(OutdatedIntent)
    )
