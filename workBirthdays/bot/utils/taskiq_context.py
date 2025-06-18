import asyncio
import random
import shutil
import string
from functools import partial
from pathlib import Path
from typing import Callable, Awaitable, Self

import aiofiles.os as aios
import aiofiles.ospath as aiopath
from aiogram import Bot
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode
from taskiq import TaskiqResultTimeoutError, TaskiqResult, AsyncTaskiqTask, AsyncTaskiqDecoratedTask

from workBirthdays.core.config import Paths
from workBirthdays.core.utils.exceptions import BaseError
from workBirthdays.core.utils.exceptions.taskiq import TaskiqTaskError


class TempFolderIsExist(BaseError):
    user_note_template = "Ошибка файловой системы. Попробуйте выполнить действие ещё раз."


class TaskiqContext:
    def __init__(
            self,
            task: AsyncTaskiqDecoratedTask,
            manager: DialogManager,
            error_log_message: str = "Ошибка выполнения задачи.",
            error_user_message: str | None = None,
            timeout_message: str | None = "Превышено время выполнения задачи.",
            error_callback: Callable[[TaskiqResult, DialogManager], Awaitable[None]] | None = None,
            raise_error: bool = True,
            timeout_callback: Callable[[DialogManager], Awaitable[None]] | None = None,
            make_temp_folder: bool = True
    ):
        self._task = task
        self._manager = manager
        self._error_log_message = error_log_message
        self._error_user_message = error_user_message
        self._timeout_message = timeout_message
        self._error_callback = error_callback
        self._raise_error = raise_error
        self._timeout_callback = timeout_callback
        self._make_temp_folder = make_temp_folder

        self._temp_folder_path: Path | None = None

    @property
    def temp_folder(self) -> Path:
        return self._temp_folder_path

    @property
    def _paths(self) -> Paths:
        return self._manager.middleware_data["paths"]

    async def __aenter__(self) -> Self:
        if self._make_temp_folder:
            temp_folder_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
            temp_folder_path = self._paths.temp_folder_path / temp_folder_name
            if not await aiopath.exists(temp_folder_path):
                await aios.mkdir(temp_folder_path)
                self._temp_folder_path = temp_folder_path
            else:
                raise TempFolderIsExist

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if await aiopath.exists(self._temp_folder_path or ""):
            loop = asyncio.get_running_loop()
            p_func = partial(shutil.rmtree, self._temp_folder_path)
            return await loop.run_in_executor(None, p_func)

    async def wait_result(self, timeout: float = -1, **task_kwargs):
        try:
            task: AsyncTaskiqTask = await self._task.kiq(**task_kwargs)
            res: TaskiqResult = await task.wait_result(timeout=timeout)
            if res.is_err:
                if self._error_callback is not None:
                    await self._error_callback(res, self._manager)
                if self._raise_error:
                    self._manager.show_mode = ShowMode.DELETE_AND_SEND
                    raise TaskiqTaskError(
                        self._error_log_message, res.error, self._error_user_message
                    )

            return res.return_value

        except TaskiqResultTimeoutError:
            self._manager.show_mode = ShowMode.DELETE_AND_SEND
            if self._timeout_callback is not None:
                await self._timeout_callback(self._manager)
            if self._timeout_message is not None:
                user: User = self._manager.middleware_data["event_from_user"]
                bot: Bot = self._manager.middleware_data["bot"]
                await bot.send_message(chat_id=user.id, text=self._timeout_message)
