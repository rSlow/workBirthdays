from aiogram import types, F
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import SwitchTo, Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.states.admin import RoleSG, AddUserToRoleSG
from workBirthdays.bot.utils.dialog_factory import choice_window_factory
from workBirthdays.bot.views import buttons as b
from workBirthdays.core.db.dao.role import RoleDao
from workBirthdays.core.db.dao.user import UserDao
from workBirthdays.core.db.dto import id_getter
from .getters import user_role_getter, role_getter, users_role_getter


async def add_user_dialog_start(_, __, manager: DialogManager):
    role_id = manager.start_data["role_id"]
    await manager.start(AddUserToRoleSG.input, {"role_id": role_id})


role_window = Window(
    Format("Роль: <u>{role.alias}</u>"),
    Format("Имя роли: <u>{role.name}</u>"),
    Format("Количество пользователей с ролью: {users_count}"),
    SwitchTo(
        Const("Список пользователей"),
        state=RoleSG.users,
        id="users",
        when=F["users_count"]
    ),
    Button(
        Const("Добавить пользователя"),
        on_click=add_user_dialog_start,
        id="add_user"
    ),
    SwitchTo(
        Const("Удалить роль"),
        state=RoleSG.delete,
        id="delete",
    ),
    b.CANCEL,
    state=RoleSG.main,
    getter=role_getter
)


async def accept_remove_user_from_role(_, __, manager: DialogManager, user_id: str):
    manager.dialog_data["user_id"] = int(user_id)
    await manager.switch_to(RoleSG.accept_delete_user)


role_users_window = Window(
    Format("Количество пользователей с ролью '{role.mention}': {users_count}"),
    ScrollingGroup(
        Select(
            Format("❌ {item.name_mention} id=({item.tg_id})"),
            id="users",
            items="users",
            item_id_getter=id_getter,
            on_click=accept_remove_user_from_role
        ),
        id="users_scroll",
        hide_on_single_page=True,
        width=1,
        height=6
    ),
    b.BACK,
    getter=users_role_getter,
    state=RoleSG.users
)


@inject
async def delete_user_from_role(
        callback: types.CallbackQuery, _, manager: DialogManager,
        role_dao: FromDishka[RoleDao], user_dao: FromDishka[UserDao],
):
    role = await role_dao.get(manager.start_data["role_id"])
    user = await user_dao.get_by_id(manager.dialog_data["user_id"])
    await role_dao.remove_user(role.id_, user.id_)

    await callback.message.answer(
        f"Пользователь '{user.name_mention}' освобожден от роли {role.mention}."
    )
    await manager.switch_to(RoleSG.users, show_mode=ShowMode.DELETE_AND_SEND)


role_user_delete_accept_window = choice_window_factory(
    Format(
        "Освободить пользователя {user.name_mention} от роли {role.mention}?"
    ),
    state=RoleSG.accept_delete_user,
    back_state=RoleSG.users,
    on_click=delete_user_from_role,  # noqa
    getter=user_role_getter
)


@inject
async def on_accept_delete(
        callback: types.CallbackQuery, _, manager: DialogManager, dao: FromDishka[RoleDao]
):
    role_id = manager.start_data["role_id"]
    role = await dao.get(role_id)
    await dao.delete(role_id)
    await callback.message.answer(f"Роль '{role.mention}' удалена.")
    await manager.done(show_mode=ShowMode.DELETE_AND_SEND)


delete_role_window = choice_window_factory(
    Format("Удаление роли '{role.mention}'."),
    Const("Вы уверены?"),
    on_click=on_accept_delete,  # noqa
    state=RoleSG.delete,
    back_state=RoleSG.main,
    getter=role_getter
)

role_dialog = Dialog(
    role_window,
    role_users_window,
    role_user_delete_accept_window,
    delete_role_window,
)
