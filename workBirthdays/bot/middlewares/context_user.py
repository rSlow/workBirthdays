import contextlib
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from sqlalchemy.exc import NoResultFound

from workBirthdays.bot.middlewares.config import MiddlewareData
from workBirthdays.core.db.dao import UserDao


class ContextUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        state: FSMContext = data["state"]
        context_user_id = await state.get_value("context_user_id")
        if context_user_id is not None:
            container = data["dishka_container"]
            user_dao = await container.get(UserDao)
            with contextlib.suppress(NoResultFound):
                user = await user_dao.get_by_tg_id(context_user_id)
                data["context_user"] = user
        else:
            await state.update_data(context_user_id=None)

        if data.get("context_user") is None:
            data["context_user"] = data["user"]

        return await handler(event, data)
