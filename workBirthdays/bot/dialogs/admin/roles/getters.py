from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.core.db.dao.role import RoleDao
from workBirthdays.core.db.dao.user import UserDao


@inject
async def role_getter(
        dialog_manager: DialogManager, role_dao: FromDishka[RoleDao], user_dao: FromDishka[UserDao],
        **__
):
    role_id = dialog_manager.start_data["role_id"]
    role = await role_dao.get(role_id)
    users_count = await user_dao.count_with_role(role_id)
    return {
        "role": role,
        "users_count": users_count
    }


@inject
async def user_role_getter(
        dialog_manager: DialogManager, role_dao: FromDishka[RoleDao], user_dao: FromDishka[UserDao],
        **__
):
    role = await role_dao.get(dialog_manager.start_data["role_id"])
    user = await user_dao.get_by_id(dialog_manager.dialog_data["user_id"])

    return {"role": role, "user": user}


@inject
async def users_role_getter(
        dialog_manager: DialogManager, role_dao: FromDishka[RoleDao], user_dao: FromDishka[UserDao],
        **__
):
    role_id = dialog_manager.start_data["role_id"]
    role = await role_dao.get(role_id)
    users = await user_dao.get_all_with_role(role_id)
    return {
        "role": role,
        "users": users,
        "users_count": len(users)
    }
