from datetime import datetime, date, time

from aiogram import types
from aiogram_dialog import DialogManager, ShowMode

from workBirthdays.core.utils import dates


def datetime_from_text(text) -> datetime:
    try:
        return datetime.strptime(text, dates.DATE_FORMAT)
    except ValueError as e:
        raise ValueError(
            f"Строка <b>{text}</b> "
            f"не соответствует формату {dates.DATETIME_FORMAT_USER}, "
            f"попробуй ещё раз."
        ) from e


def date_from_text(text) -> date:
    try:
        return datetime.strptime(text, dates.DATE_FORMAT).date()
    except ValueError as e:
        raise ValueError(
            f"Строка <b>{text}</b> "
            f"не соответствует формату {dates.DATE_FORMAT_USER}, "
            f"попробуй ещё раз."
        ) from e


def time_from_text(text) -> time:
    try:
        return datetime.strptime(text, dates.TIME_FORMAT).time()
    except ValueError as e:
        raise ValueError(
            f"Строка <b>{text}</b> "
            f"не соответствует формату {dates.TIME_FORMAT_USER}, "
            f"попробуй ещё раз."
        ) from e


async def error_dt_input_handler(
        message: types.Message, _, manager: DialogManager, error: ValueError
):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer(error.args[0])
