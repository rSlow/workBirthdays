from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from sqlalchemy.exc import NoResultFound

from workBirthdays.bot.middlewares.config import MiddlewareData
from workBirthdays.bot.states.birthdays import AddUserContextSG, RemoveUserContextSG
from workBirthdays.bot.utils.dialog_factory import choice_dialog_factory
from workBirthdays.bot.views import buttons
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao import UserDao, RoleDao


@inject
async def on_user_id_input(
        message: types.Message, _widget: ManagedTextInput[int], manager: DialogManager,
        user_id: int, user_dao: FromDishka[UserDao], role_dao: FromDishka[RoleDao],
):
    try:
        user = await user_dao.get_by_tg_id(user_id)
        await message.answer(f"Выбран контекст пользователя {user.short_mention}.")

    except NoResultFound:
        user = dto.User(tg_id=user_id, is_bot=False, is_active=True)
        db_user = await user_dao.upsert_user(user)
        birthdays_role = await role_dao.get_by_name("birthdays")
        await role_dao.add_user(birthdays_role.id_, db_user.id_)
        await message.answer(f"Создан пользователь c ID={user.tg_id}.")
        await message.answer(f"Выбран контекст пользователя c ID={user.tg_id}.")

    state: FSMContext = manager.middleware_data["state"]
    await state.update_data(context_user_id=user_id)
    await manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_user_id_error(
        message: types.Message, _widget: ManagedTextInput[str], _manager: DialogManager,
        error: ValueError
):
    await message.answer(f"Telegram ID {error.args[0]} недействителен.")


def user_id_tf(value: str):
    try:
        return int(value)
    except ValueError:
        return ValueError(value)


add_user_context_dialog = Dialog(
    Window(
        Const("Введите TG ID необходимого пользователя"),
        buttons.CANCEL,
        TextInput(
            id="user_id_input",
            on_success=on_user_id_input,
            on_error=on_user_id_error,
            type_factory=user_id_tf
        ),
        state=AddUserContextSG.state
    )
)


async def remove_user_context_getter(context_user: dto.User, **__):
    return {"context_user_id": context_user.tg_id}


async def on_remove_user_context(_c: CallbackQuery, _b: Button, manager: DialogManager):
    middleware_data: MiddlewareData = manager.middleware_data
    state = middleware_data["state"]
    context_user = middleware_data["context_user"]
    await state.update_data(context_user_id=None)
    await _c.message.answer(f"Контекст пользователя с ID={context_user.tg_id} завершен.")
    await manager.done(show_mode=ShowMode.DELETE_AND_SEND)


remove_user_context_dialog = choice_dialog_factory(
    Format("Выйти из контекста пользователя с ID={context_user_id}?"),
    state=RemoveUserContextSG.state,
    on_click=on_remove_user_context,
    getter=remove_user_context_getter
)
