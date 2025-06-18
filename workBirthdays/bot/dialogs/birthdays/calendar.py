from datetime import date

from aiogram_dialog import Window, Dialog, DialogManager, ChatEvent, ShowMode
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.di.jinja import JinjaRenderer
from workBirthdays.bot.states.birthdays import CalendarSG
from workBirthdays.bot.views import buttons as b
from workBirthdays.bot.views.types import LocalizedCalendar
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao.birthday import BirthdayDao


@inject
async def on_date_selected(
        callback: ChatEvent, _, manager: DialogManager, selected_date: date,
        jinja: FromDishka[JinjaRenderer], dao: FromDishka[BirthdayDao]
):
    user: dto.User = manager.middleware_data["user"]
    birthdays = await dao.get_by_date(d=selected_date, user_id=user.id_)
    if not birthdays:
        return await callback.answer("Нет дней рождения.", show_alert=True)
    message_text = jinja.render_template(
        "birthdays/main_query.jinja2",
        dates={selected_date: birthdays}
    )
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await callback.message.answer(message_text)


calendar_dialog = Dialog(
    Window(
        Const("Выберите дату для проверки:"),
        LocalizedCalendar(
            id="cal",
            on_click=on_date_selected,  # noqa
        ),
        b.CANCEL,
        state=CalendarSG.state
    )
)
