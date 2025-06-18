from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.states.admin import AddUserToRoleSG
from workBirthdays.bot.views import buttons as b
from workBirthdays.core.db.dao.role import RoleDao
from workBirthdays.core.db.dao.user import UserDao
from workBirthdays.core.utils.exceptions.user import UnknownUserError
from .getters import user_role_getter


@inject
async def handle_user_input(
        message: types.Message, __, manager: DialogManager, input_: str,
        dao: FromDishka[UserDao],
):
    manager.show_mode = ShowMode.DELETE_AND_SEND

    try:

        try:
            user_id = int(input_)
            user = await dao.get_by_tg_id(user_id)
        except ValueError:  # `input_` is not `int`
            user = await dao.get_by_username(input_)

    except UnknownUserError:
        return await message.answer("Пользователь не найден, проверьте данные.")

    manager.dialog_data["user_id"] = user.id_
    await manager.next()


user_input_window = Window(
    Const("Введите TelegramID пользователя или его username..."),
    TextInput(
        id="user_input",
        on_success=handle_user_input  # noqa
    ),
    b.CANCEL,
    state=AddUserToRoleSG.input
)


@inject
async def accept_user_role(
        callback: types.CallbackQuery, __, manager: DialogManager,
        role_dao: FromDishka[RoleDao], user_dao: FromDishka[UserDao]
):
    role = await role_dao.get(manager.start_data["role_id"])
    user = await user_dao.get_by_id(manager.dialog_data["user_id"])
    await role_dao.add_user(role.id_, user.id_)
    await callback.message.answer(
        f"Пользователю {user.name_mention} добавлена роль {role.mention}."
    )
    await manager.done(show_mode=ShowMode.DELETE_AND_SEND)


user_accept_window = Window(
    Format("Добавить роль '{role.mention}' пользователю {user.name_mention}?"),
    Button(
        Const("Добавить"),
        on_click=accept_user_role,  # noqa
        id="accept_user_role",
    ),
    Cancel(
        Const("Отмена")
    ),
    getter=user_role_getter,
    state=AddUserToRoleSG.accept
)

add_user_to_role_dialog = Dialog(
    user_input_window,
    user_accept_window
)
