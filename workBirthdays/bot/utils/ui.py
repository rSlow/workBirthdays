import logging

from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats

from workBirthdays.bot.views import commands

logger = logging.getLogger(__name__)


async def setup(bot: Bot):
    _commands = [
        commands.BIRTHDAYS,
        commands.START,
        commands.HELP,
        commands.ABOUT,
        commands.UPDATE,
    ]
    await bot.set_my_commands(commands=_commands, scope=BotCommandScopeAllPrivateChats())
    logger.info("%s bot commands were installed.", len(_commands))
