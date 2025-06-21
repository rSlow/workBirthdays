from aiogram import types
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.states.birthdays import ClearBirthdaysSG
from workBirthdays.bot.utils.dialog_factory import choice_dialog_factory
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao.birthday import BirthdayDao


@inject
async def clear_birthdays(
        callback: types.CallbackQuery, _, manager: DialogManager, dao: FromDishka[BirthdayDao]
):
    user: dto.User = manager.middleware_data["context_user"]
    await dao.delete_all_from_user(user.id_)
    await callback.message.answer("Все дни рождения удалены.")
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


clear_dialog = choice_dialog_factory(
    Const("Очистка всех данных о днях рождения."),
    Const("Вы уверены?"),
    state=ClearBirthdaysSG.state,
    on_click=clear_birthdays
)
