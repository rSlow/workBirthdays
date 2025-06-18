import asyncio
import secrets
from abc import ABC, abstractmethod
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import FastAPI, Request, Response, APIRouter, Header


class BaseRequestHandler(ABC):
    def __init__(self, **data: Any) -> None:
        self.data = data
        self._background_feed_update_tasks: set[asyncio.Task[Any]] = set()

    @abstractmethod
    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        pass

    def register(self, app: FastAPI, /, path: str, **kwargs: Any) -> None:
        router = APIRouter()
        router.add_api_route(methods=["POST"], path=path, endpoint=self.handle, **kwargs)
        app.include_router(router)

    @staticmethod
    async def _build_response_content(
            bot: Bot, dispatcher: Dispatcher,
            result: TelegramMethod[TelegramType] | None
    ) -> Any:
        if result:
            await dispatcher.silent_call_request(bot, result)

    async def _handle_request(self, bot: Bot, dispatcher: Dispatcher, request: Request) -> Response:
        result: TelegramMethod[Any] | None = \
            await dispatcher.feed_webhook_update(
                bot,
                await request.json(),
                **self.data,
            )
        content = await self._build_response_content(bot=bot, dispatcher=dispatcher, result=result)
        return Response(content=content)

    @inject
    async def handle(
            self,
            request: Request,
            bot: FromDishka[Bot],
            dispatcher: FromDishka[Dispatcher],
            secret_token: str = Header(
                default="",
                alias="X-Telegram-Bot-Api-Secret-Token"
            )
    ) -> Response:
        if not self.verify_secret(secret_token, bot):
            return Response(content="Unauthorized", status_code=401)
        return await self._handle_request(bot=bot, dispatcher=dispatcher, request=request)

    __call__ = handle


class SimpleRequestHandler(BaseRequestHandler):
    def __init__(self, secret_token: str | None = None, **data: Any):
        """
        Handler for single Bot instance

        :param dispatcher: instance of :class:
            `aiogram.dispatcher.dispatcher.Dispatcher`
        :param handle_in_background: immediately responds to the Telegram
            instead of a waiting end of handler process
        :param bot: instance of :class:`aiogram.client.bot.Bot`
        """
        super().__init__(**data)
        self.secret_token = secret_token

    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        if self.secret_token:
            return secrets.compare_digest(telegram_secret_token, self.secret_token)
        return True
