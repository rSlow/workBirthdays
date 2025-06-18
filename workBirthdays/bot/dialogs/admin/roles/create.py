from aiogram import types
from aiogram_dialog import Window, DialogManager, Dialog, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.states.admin import RoleCreateSG
from workBirthdays.bot.views import buttons as b
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao.role import RoleDao


async def on_role_alias_success(_, __, manager: DialogManager, role_alias: str):
    manager.dialog_data["role_alias"] = role_alias
    await manager.next()


create_role_alias_window = Window(
    Const("Введите отображаемое название роли:"),
    b.CANCEL,
    TextInput(
        on_success=on_role_alias_success,
        id="role_alias"
    ),
    state=RoleCreateSG.alias
)


@inject
async def save_role(
        message: types.Message, _, manager: DialogManager, role_name: str,
        dao: FromDishka[RoleDao]
):
    role_alias = manager.dialog_data["role_alias"]
    role = dto.UserRole(name=role_name, alias=role_alias)
    created_role = await dao.add(role)
    await message.answer(f"Роль '{created_role.alias}' создана.")
    await manager.done(show_mode=ShowMode.DELETE_AND_SEND)


create_role_name_window = Window(
    Const("Введите служебное имя роли:"),
    b.BACK,
    TextInput(
        on_success=save_role,  # noqa
        id="role_name"
    ),
    state=RoleCreateSG.name
)

create_role_dialog = Dialog(
    create_role_alias_window,
    create_role_name_window,
)
