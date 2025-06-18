from aiogram import Router

from .add_user import add_user_to_role_dialog
from .create import create_role_dialog
from .role import role_dialog
from .start import role_manager_start_dialog


def setup():
    router = Router(name=__name__)

    router.include_router(role_manager_start_dialog)
    router.include_router(create_role_dialog)
    router.include_router(role_dialog)
    router.include_router(add_user_to_role_dialog)

    return router
