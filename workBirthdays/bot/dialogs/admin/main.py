import os.path

from aiogram import types
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from workBirthdays.bot.states.admin import AdminMainSG, RoleManagerStartSG
from workBirthdays.bot.views import buttons as b
from workBirthdays.core.config import Paths


@inject
async def get_logs(
        callback: types.CallbackQuery, _, manager: DialogManager, paths: FromDishka[Paths]
):
    files = [
        types.FSInputFile(path=filename, filename=filename.name)
        for filename in paths.log_path.glob("*.log")
        if os.path.getsize(filename)  # check file is not empty
    ]

    if not files:
        return await callback.answer("Нет файлов логов :(")

    media = [types.InputMediaDocument(media=file) for file in files]
    await callback.message.answer_media_group(media)
    manager.show_mode = ShowMode.DELETE_AND_SEND


admin_main_dialog = Dialog(
    Window(
        Const("Выберите действие:"),
        Button(
            Const("Файлы логов"),
            id="logs",
            on_click=get_logs  # noqa
        ),
        Start(
            Const("Менеджер ролей"),
            id="role_manager",
            state=RoleManagerStartSG.main
        ),
        b.MAIN_MENU,
        state=AdminMainSG.state
    )
)
