import logging
from functools import partial

import uvicorn
from aiogram import Bot, Dispatcher
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka

from workBirthdays.api import create_app as create_api_app, ApiAppConfig
from workBirthdays.api.config.models import ApiConfig
from workBirthdays.api.config.parser.main import load_config as load_api_config
from workBirthdays.api.di import get_api_providers
from workBirthdays.api.utils.webhook.handler import SimpleRequestHandler
from workBirthdays.api.utils.webhook.setup import setup_lifespan
from workBirthdays.bot.config.models import BotAppConfig
from workBirthdays.bot.config.models.webhook import WebhookConfig
from workBirthdays.bot.config.parser.main import load_config as load_bot_config
from workBirthdays.bot.di import get_bot_providers
from workBirthdays.bot.di.dp import resolve_update_types
from workBirthdays.bot.utils import ui
from workBirthdays.core.config.parser.config_logging import setup_logging
from workBirthdays.core.config.parser.paths import get_paths
from workBirthdays.core.config.parser.retort import get_base_retort
from workBirthdays.core.db.dao.user import UserDao
from workBirthdays.core.di import get_common_providers
from workBirthdays.core.scheduler.scheduler import ApScheduler
from workBirthdays.core.utils import di_visual
from workBirthdays.mq.broker import broker

logger = logging.getLogger(__name__)


def main():
    paths = get_paths()
    setup_logging(paths)

    retort = get_base_retort()
    api_config = load_api_config(paths, retort)
    bot_config = load_bot_config(paths, retort)
    webhook_config = bot_config.bot.webhook

    di_container = make_async_container(
        *get_common_providers(bot_config),
        *get_bot_providers(),
        *get_api_providers(),
        context={
            ApiAppConfig: api_config,
            BotAppConfig: bot_config,
        }
    )

    api_app = create_api_app(api_config)
    setup_lifespan(api_app, di_container)

    webhook_handler = SimpleRequestHandler(secret_token=webhook_config.secret)
    webhook_handler.register(api_app, webhook_config.path)

    setup_fastapi_dishka(di_container, api_app)

    startup_callback = partial(on_startup, di_container, bot_config, api_config.api, webhook_config)
    shutdown_callback = partial(on_shutdown, di_container)
    api_app.add_event_handler("startup", startup_callback)
    api_app.add_event_handler("shutdown", shutdown_callback)

    logger.info(
        "app prepared with dishka:\n%s",
        di_visual.render(
            [di_container.registry, *di_container.child_registries],
        ),
    )
    return api_app


async def on_startup(
        dishka: AsyncContainer,
        bot_config: BotAppConfig, api_config: ApiConfig,
        webhook_config: WebhookConfig
):
    web_config = bot_config.web
    webhook_url = (
            web_config.real_base_url +  # domain + proxy
            api_config.root_path + webhook_config.path
    )

    bot = await dishka.get(Bot)
    dp: Dispatcher = await dishka.get(Dispatcher)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=webhook_url,
        secret_token=webhook_config.secret,
        allowed_updates=resolve_update_types(dp),
    )
    logger.info("as webhook url used %s", webhook_url)

    await ui.setup(bot)
    await broker.startup()

    await dishka.get(ApScheduler)  # run scheduler

    async with dishka() as request_dishka:
        user_dao = await request_dishka.get(UserDao)
        await user_dao.set_superusers(bot_config.bot.superusers)


async def on_shutdown(dishka: AsyncContainer):
    bot: Bot = await dishka.get(Bot)
    await bot.delete_webhook()
    logger.info("webhook deleted")

    await dishka.close()


def run():
    uvicorn.run(
        app="workBirthdays.__main__:main",
        host="0.0.0.0",
        port=8000,
        factory=True
    )


if __name__ == '__main__':
    run()
