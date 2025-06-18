from dataclasses import dataclass

from workBirthdays.bot.config.models.bot import BotConfig
from workBirthdays.bot.config.models.storage import StorageConfig
from workBirthdays.core.config import BaseConfig


@dataclass
class BotAppConfig(BaseConfig):
    bot: BotConfig
    storage: StorageConfig

    @classmethod
    def from_base(
            cls, base: BaseConfig, bot: BotConfig, storage: StorageConfig
    ):
        return cls(
            paths=base.paths, db=base.db, redis=base.redis, app=base.app, web=base.web,
            auth=base.auth,
            bot=bot, storage=storage
        )
