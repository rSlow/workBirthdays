from typing import Any

from adaptix import Retort

from ..models.auth import SecurityConfig


def load_auth_config(
        config_dct: dict[str, Any], base_url: str,
        bot_token: str, retort: Retort
) -> SecurityConfig:
    config_dct["domain"] = base_url
    config_dct["tg-bot-token"] = bot_token
    return retort.load(config_dct, SecurityConfig)
