from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Start, Column
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.di.jinja import JinjaRenderer
from workBirthdays.bot.filters.user import F_User
from workBirthdays.bot.states.birthdays import (
    TimeCorrectionSG, ClearBirthdaysSG, BirthdaysNotificationSG, CalendarSG,
    BirthdaysMenuSG, AddUserContextSG, RemoveUserContextSG
)
from workBirthdays.bot.views import buttons as b
from workBirthdays.bot.views.birthdays import get_birthdays_message
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao.birthday import BirthdayDao


@inject
async def check_birthdays_callback(
        callback: types.CallbackQuery, _, manager: DialogManager,
        dao: FromDishka[BirthdayDao], jinja: FromDishka[JinjaRenderer],
):
    user: dto.User = manager.middleware_data["context_user"]
    message_text = await get_birthdays_message(dao, user.id_, jinja)
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await callback.message.answer(message_text)


async def main_window_getter(state: FSMContext, **__):
    context_user_id = await state.get_value("context_user_id")
    return {"context_user_id": context_user_id}


main_birthday_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Column(
            Button(
                Const("Проверить ДР 🎈"),
                id="check",
                on_click=check_birthdays_callback
            ),
            Start(
                Const("Календарь 📆"),
                id="calendar",
                state=CalendarSG.state
            ),
            Start(
                Const("Оповещения 🕓"),
                id="notifications",
                state=BirthdaysNotificationSG.state
            ),
            Start(
                Const("Очистить данные 🗑"),
                id="clear_data",
                state=ClearBirthdaysSG.state
            ),
            Start(
                Const("Установка часового пояса 🌏"),
                id="time_correction",
                state=TimeCorrectionSG.state
            ),

            Start(
                Const("Войти в контекст пользователя 🧍"),
                id="add_user_context",
                state=AddUserContextSG.state,
                when=F_User.is_superuser & F["context_user_id"].is_(None)
            ),
            Start(
                Const("Выйти из контекста пользователя 🚫"),
                id="remove_user_context",
                state=RemoveUserContextSG.state,
                when=F_User.is_superuser & F["context_user_id"].is_not(None)
            ),
            b.MAIN_MENU,
        ),
        state=BirthdaysMenuSG.state,
        getter=main_window_getter
    )
)
