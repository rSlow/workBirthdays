from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.kbd import Column, Start
from aiogram_dialog.widgets.text import Format, Const

from workBirthdays.bot.filters.user import F_User, adg_role_filter
from workBirthdays.bot.states.admin import AdminMainSG
from workBirthdays.bot.states.birthdays import BirthdaysMenuSG
from workBirthdays.bot.states.start import MainMenuSG
from workBirthdays.bot.states.users import UserMainSG
from workBirthdays.core.db import dto


async def main_menu_getter(user: dto.User, **__):
    return {"mention": user.short_mention}


main_menu = Dialog(
    Window(
        Format("{mention}, выберите действие:"),
        Column(
            Start(
                Const("Дни рождений 🎂"),
                id="birthdays",
                state=BirthdaysMenuSG.state,
                when=adg_role_filter("birthdays")
            ),
            Start(
                Const("Профиль 👤"),
                id="user_profile",
                state=UserMainSG.state,
            ),
            Start(
                Const("Админка ⚙️"),
                id="admin",
                state=AdminMainSG.state,
                when=F_User.is_superuser
            ),
        ),
        getter=main_menu_getter,
        state=MainMenuSG.state,
    ),
    launch_mode=LaunchMode.ROOT
)
