import json

from aiogram.types import TelegramObject
from aiogram.utils.markdown import html_decoration as hd


def get_update_text(event: TelegramObject):
    return hd.quote(
        json.dumps(
            event.model_dump(exclude_none=True),
            default=str, ensure_ascii=False
        )[:3500]
    )
