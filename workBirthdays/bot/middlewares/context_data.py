from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog.api.entities import DialogUpdateEvent

from workBirthdays.bot.config.models import BotConfig
from workBirthdays.bot.di.jinja import JinjaRenderer
from workBirthdays.bot.middlewares.config import MiddlewareData
from workBirthdays.bot.views.alert import BotAlert
from workBirthdays.core.config import Paths
from workBirthdays.core.db import dto
from workBirthdays.core.db.dao import DaoHolder
from workBirthdays.core.scheduler.scheduler import ApScheduler
from workBirthdays.core.utils.lock_factory import LockFactory


class ContextDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        dishka = data["dishka_container"]
        dao_holder: DaoHolder = await dishka.get(DaoHolder)
        data["bot_config"] = await dishka.get(BotConfig)
        data["locker"] = await dishka.get(LockFactory)
        data["scheduler"] = await dishka.get(ApScheduler)
        data["jinja_renderer"] = await dishka.get(JinjaRenderer)
        data["alert"] = await dishka.get(BotAlert)
        data["paths"] = await dishka.get(Paths)
        data["dao"] = dao_holder

        user_tg = data.get("event_from_user", None)
        if user_tg is None:
            user = None
        else:
            if isinstance(event, DialogUpdateEvent):
                user = await dao_holder.user.get_by_tg_id(user_tg.id)
            else:
                user = await dao_holder.user.upsert_user(dto.User.from_aiogram(user_tg))
        data["user"] = user

        return await handler(event, data)
