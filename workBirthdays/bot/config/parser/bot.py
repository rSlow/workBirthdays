from typing import Any

from adaptix import Retort

from ..models.bot import BotConfig


def load_bot_config(
        config_dct: dict[str, Any], base_url: str, retort: Retort
) -> BotConfig:
    config_dct["webhook"]["base-url"] = base_url
    return retort.load(config_dct, BotConfig)
