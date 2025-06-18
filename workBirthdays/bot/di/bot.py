import logging
from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide, from_context

from workBirthdays.bot.config.models.bot import BotConfig
from workBirthdays.bot.config.models.main import BotAppConfig
from workBirthdays.bot.config.models.storage import StorageConfig
from workBirthdays.bot.views.alert import BotAlert

logger = logging.getLogger(__name__)


class BotProvider(Provider):
    scope = Scope.APP

    bot_config = from_context(BotAppConfig)

    @provide
    def get_bot_config(self, config: BotAppConfig) -> BotConfig:
        return config.bot

    @provide
    def get_bot_storage_config(self, config: BotAppConfig) -> StorageConfig:
        return config.storage

    @provide
    async def get_bot(self, bot_config: BotConfig) -> AsyncIterable[Bot]:
        bot = Bot(
            token=bot_config.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML, allow_sending_without_reply=True
            )
        )
        yield bot
        await bot.session.close()

    @provide
    async def bot_alert(self, bot: Bot, bot_config: BotConfig) -> BotAlert:
        return BotAlert(bot, bot_config.log_chat)
