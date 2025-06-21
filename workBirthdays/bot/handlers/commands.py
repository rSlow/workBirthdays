from aiogram import types, Router, Bot
from aiogram.filters import Command
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog import StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from workBirthdays.bot.di.jinja import JinjaRenderer
from workBirthdays.bot.states.start import MainMenuSG
from workBirthdays.bot.views import commands
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao import EventLogDao


@inject
async def cmd_start(
        message: types.Message, dialog_manager: DialogManager, user: dto.User, bot: Bot,
        dao: FromDishka[EventLogDao], jinja: FromDishka[JinjaRenderer],
):
    start_event = await dao.get_last_by_user(user.tg_id, "/start")
    if start_event is None:
        welcome_message = jinja.render_template(
            "commands/start.jinja2",
            {"bot_name": (await bot.get_my_name()).name}
        )
        await message.answer(welcome_message)

    await dialog_manager.start(state=MainMenuSG.state, mode=StartMode.RESET_STACK)


@inject
async def cmd_help(
        message: types.Message, dialog_manager: DialogManager,
        jinja: FromDishka[JinjaRenderer]
):
    help_message = jinja.render_template("commands/help.jinja2")
    await message.answer(help_message)
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_about(message: types.Message, dialog_manager: DialogManager):
    await message.answer(f"Разработчик бота - @rs1ow.\n")
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_update(message: types.Message, dialog_manager: DialogManager):
    await message.delete()
    await dialog_manager.update({}, show_mode=ShowMode.DELETE_AND_SEND)


def setup():
    router = Router(name=__name__)

    router.message.register(cmd_start, Command(commands.START))
    router.message.register(cmd_help, Command(commands.HELP))
    router.message.register(cmd_about, Command(commands.ABOUT))
    router.message.register(cmd_update, Command(commands.UPDATE))

    return router
