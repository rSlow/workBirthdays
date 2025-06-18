__all__ = [
    "get_bot_providers",
]

from dishka import Provider

from .bot import BotProvider
from .dp import DpProvider
from .jinja import JinjaProvider


def get_bot_providers() -> list[Provider]:
    return [
        BotProvider(),
        DpProvider(),
        JinjaProvider()
    ]
