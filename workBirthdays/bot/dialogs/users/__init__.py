from aiogram import Router

from .main import user_profile_dialog
from .password import set_password_dialog


def setup():
    router = Router(name=__name__)

    router.include_routers(
        user_profile_dialog,
        set_password_dialog,
    )

    return router
