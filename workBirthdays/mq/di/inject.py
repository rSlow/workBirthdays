__all__ = [
    "inject",
    "error_inject"
]

from collections.abc import Callable
from typing import TypeVar, ParamSpec, cast, Any

from dishka.integrations.base import wrap_injection
from dishka.integrations.taskiq import inject as taskiq_inject, CONTAINER_NAME
from taskiq import TaskiqMessage
from taskiq.result.v2 import TaskiqResult

from workBirthdays.mq.utils.types.di import ExceptionHandler

T = TypeVar("T")
P = ParamSpec("P")

InjectFunction = Callable[[Callable[P, T]], Callable[P, T]]

inject = cast(InjectFunction, taskiq_inject)


def _error_container_getter(
        args: tuple[BaseException, TaskiqMessage, TaskiqResult],
        __: dict[str, Any]
):
    _exc, _msg, result = args
    return result.labels[CONTAINER_NAME]


def error_inject(func: ExceptionHandler) -> ExceptionHandler:
    return wrap_injection(  # noqa
        func=func,
        is_async=True,
        remove_depends=True,
        container_getter=_error_container_getter,
    )
