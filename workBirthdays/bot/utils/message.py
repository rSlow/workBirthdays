import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, Chat
from aiogram_dialog import DialogManager

logger = logging.getLogger(__name__)


async def edit_dialog_message(
        manager: DialogManager, text: str, reply_markup: InlineKeyboardMarkup | None = None
):
    dialog_message_id: int = manager.current_stack().last_message_id
    bot: Bot = manager.middleware_data["bot"]
    chat: Chat = manager.middleware_data["event_chat"]
    return await bot.edit_message_text(
        chat_id=chat.id,
        message_id=dialog_message_id,
        text=text,
        reply_markup=reply_markup
    )


async def delete_message(bot: Bot, chat_id: int, message_id: int, error_text: str | None = None):
    try:
        return await bot.delete_message(chat_id=chat_id, message_id=message_id)

    except TelegramBadRequest as ex:
        logger.warning(
            error_text.format_map({
                "ex": ex,
                "message_id": message_id,
                "chat_id": chat_id
            })
            if error_text
            else f"Error while deleting message {message_id}: {ex.message}"
        )
