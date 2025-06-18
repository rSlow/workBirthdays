from dataclasses import dataclass
from datetime import datetime

import pytz
from aiogram import types as t
from aiogram_dialog.utils import CB_SEP

from workBirthdays.core.db import dto


@dataclass
class LogEvent:
    type_: str
    chat_id: int
    dt: datetime
    user_id: int | None = None
    content_type: str | None = None
    data: str | None = None

    @classmethod
    def from_message(cls, message: t.Message):
        return cls(
            type_="message",
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            content_type=message.content_type,
            dt=message.date,
            data=message.text
        )

    @classmethod
    def from_callback_query(cls, callback: t.CallbackQuery):
        dt = datetime.now(tz=pytz.UTC)
        chat_id = callback.message.chat.id
        if isinstance(callback.message, t.InaccessibleMessage):
            return dto.LogEvent(
                type_="inaccessible_callback_query",
                chat_id=chat_id,
                dt=dt
            )
        if callback.data and CB_SEP in callback.data:
            data = callback.data.split(CB_SEP, maxsplit=1)[1]
        else:
            data = callback.data

        return cls(
            type_="callback_query",
            user_id=callback.from_user.id,
            chat_id=chat_id,
            dt=dt,
            data=data
        )
