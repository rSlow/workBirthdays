from aiogram import types, F
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const, Case
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.api.utils.auth import AuthService
from workBirthdays.bot.states.users import UserMainSG, SetPassword
from workBirthdays.bot.views import buttons as b
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao.user import UserDao


@inject
async def main_window_getter(context_user: dto.User, user_dao: FromDishka[UserDao], **__):
    user_with_creds = await user_dao.get_by_tg_id_with_password(context_user.tg_id)
    return {"has_password": user_with_creds.hashed_password is not None}


@inject
async def send_token(
        callback: types.CallbackQuery, _, manager: DialogManager,
        auth: FromDishka[AuthService], dao: FromDishka[UserDao]
):
    user: dto.User = manager.middleware_data["context_user"]
    user_with_creds = await dao.get_by_tg_id_with_password(user.tg_id)
    basic = auth.create_user_basic_token(user_with_creds)
    token = basic.split(" ", maxsplit=1)[1]
    await callback.message.answer(f"Токен внешней авторизации:\n<pre>{token}</pre>")
    manager.show_mode = ShowMode.DELETE_AND_SEND


user_profile_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Button(
            text=Const("🔐 Токен авторизации"),
            id="auth_token",
            on_click=send_token,  # noqa
            when=F["has_password"]
        ),
        Start(
            text=Case(
                {
                    True: Const("Сменить пароль"),
                    ...: Const("Установить пароль")
                },
                selector="has_password"
            ),
            id="password",
            state=SetPassword.state
        ),
        b.CANCEL,
        state=UserMainSG.state,
        getter=main_window_getter
    )
)
