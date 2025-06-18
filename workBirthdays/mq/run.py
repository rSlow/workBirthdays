import logging
import subprocess

from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from taskiq import TaskiqEvents

from workBirthdays.bot.config.models import BotAppConfig
from workBirthdays.bot.config.parser.main import load_config as load_bot_config
from workBirthdays.bot.di import get_bot_providers
from workBirthdays.core.config.parser.paths import get_paths
from workBirthdays.core.config.parser.retort import get_base_retort
from workBirthdays.core.di import get_common_providers
from workBirthdays.mq import middlewares
from workBirthdays.mq.broker import broker
from workBirthdays.mq.config.models.main import TaskiqAppConfig
from workBirthdays.mq.config.parser.main import load_config as load_taskiq_config
from workBirthdays.mq.di import get_taskiq_providers

logger = logging.getLogger("taskiq")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def worker_startup(*_):
    paths = get_paths()
    retort = get_base_retort()
    taskiq_config = load_taskiq_config(paths, retort)
    bot_config = load_bot_config(paths, retort)

    di_container = make_async_container(
        *get_common_providers(app_config=taskiq_config),
        *get_taskiq_providers(),
        *get_bot_providers(),
        context={
            TaskiqAppConfig: taskiq_config,
            BotAppConfig: bot_config
        }
    )
    setup_taskiq_dishka(di_container, broker)

    middlewares.setup(broker)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def worker_shutdown(*_):
    logger.info("Shutting down")


if __name__ == '__main__':
    subprocess.call(
        ["taskiq", "worker", "--tasks-pattern", "['**/tasks']", "workBirthdays.mq.run:broker"],
    )
