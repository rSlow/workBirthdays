from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.states.admin import RoleManagerStartSG, RoleSG, RoleCreateSG
from workBirthdays.bot.views import buttons as b
from workBirthdays.core.db.dao.role import RoleDao
from workBirthdays.core.db.dto import id_getter

role_manager_main_window = Window(
    Const("Менеджер ролей. Выберите действие:"),
    SwitchTo(
        text=Const("Список ролей"),
        id="list",
        state=RoleManagerStartSG.list
    ),
    Start(
        text=Const("Создать роль"),
        id="create",
        state=RoleCreateSG.alias
    ),
    b.CANCEL,
    state=RoleManagerStartSG.main
)


@inject
async def role_list_getter(role_dao: FromDishka[RoleDao], **__):
    roles = await role_dao.get_all()
    return {
        "roles": roles,
        "count": len(roles)
    }


async def select_role(_, __, manager: DialogManager, role_id: str):
    await manager.start(RoleSG.main, {"role_id": int(role_id)})


role_list_window = Window(
    Format("Всего ролей: {count}"),
    ScrollingGroup(
        Select(
            Format("{item.alias}"),
            id="role",
            items="roles",
            item_id_getter=id_getter,
            on_click=select_role,
        ),
        id="roles",
        width=1,
        height=6,
        hide_on_single_page=True
    ),
    SwitchTo(
        Const("Назад ◀"),
        id="__back__",
        state=RoleManagerStartSG.main
    ),
    state=RoleManagerStartSG.list,
    getter=role_list_getter
)

role_manager_start_dialog = Dialog(
    role_manager_main_window,
    role_list_window
)
