from typing import TypedDict, Any

from aiogram import types, Bot, Router
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Stack, Context
from aiogram_dialog.context.storage import StorageProxy
from dishka import AsyncContainer
from faststream.broker.core.abc import ABCBroker

from workBirthdays.bot.config.models import BotConfig
from workBirthdays.bot.di.jinja import JinjaRenderer
from workBirthdays.bot.views.alert import BotAlert
from workBirthdays.core.config import Paths
from workBirthdays.core.db import dto
from workBirthdays.core.scheduler.scheduler import Scheduler
from workBirthdays.core.utils.lock_factory import LockFactory


class AiogramMiddlewareData(TypedDict, total=False):
    event_from_user: types.User
    event_chat: types.Chat
    bot: Bot
    fsm_storage: BaseStorage
    state: FSMContext
    raw_state: Any
    handler: HandlerObject
    event_update: types.Update
    event_router: Router


class DialogMiddlewareData(AiogramMiddlewareData, total=False):
    dialog_manager: DialogManager
    aiogd_storage_proxy: StorageProxy
    aiogd_stack: Stack
    aiogd_context: Context


class MiddlewareData(DialogMiddlewareData, total=False):
    dishka_container: AsyncContainer

    locker: LockFactory
    alert: BotAlert
    scheduler: Scheduler
    jinja_renderer: JinjaRenderer
    mq: ABCBroker
    paths: Paths

    bot_config: BotConfig

    user: dto.User | None
    context_user: dto.User | None
