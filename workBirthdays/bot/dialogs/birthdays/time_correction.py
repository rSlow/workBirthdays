from datetime import time

from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.states.birthdays import TimeCorrectionSG
from workBirthdays.bot.utils.input_validation import time_from_text, error_dt_input_handler
from workBirthdays.bot.views import buttons as b
from workBirthdays.bot.views.types import JinjaTemplate
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao.notification import UserNotificationDao
from workBirthdays.core.scheduler.scheduler import ApScheduler
from workBirthdays.core.utils import dates
from workBirthdays.core.utils.dates import get_timeshift


@inject
async def success_handler(
        message: types.Message, _, manager: DialogManager, valid_time: time,
        dao: FromDishka[UserNotificationDao], scheduler: FromDishka[ApScheduler]
):
    user: dto.User = manager.middleware_data["user"]
    timeshift = get_timeshift(valid_time)
    user_state = await dao.add_or_update_user_state(user.id_, timeshift)
    notifications = await dao.get_user_notifications(user.id_)
    scheduler.update_user_birthdays(user_state, notifications)

    await message.answer(f"Часовой пояс c временем {valid_time:{dates.TIME_FORMAT}} сохранен.")
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


time_correction_dialog = Dialog(
    Window(
        JinjaTemplate("birthdays/time_correction.jinja2"),
        TextInput(
            id="timeshift",
            type_factory=time_from_text,
            on_success=success_handler,  # noqa
            on_error=error_dt_input_handler
        ),
        b.CANCEL,
        state=TimeCorrectionSG.state
    )
)
