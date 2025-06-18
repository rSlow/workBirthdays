import typing as t
from abc import ABC
from functools import wraps
from inspect import iscoroutinefunction

from dishka import AsyncContainer, Container
from dishka.integrations.base import wrap_injection

T = t.TypeVar("T")
P = t.ParamSpec("P")


class BaseInjectContext(ABC):
    # @bomzheg, it's laugh)
    """
    ATTENTION!
    GLOBAL VARIABLE!
    """

    container: Container | AsyncContainer | None = None

    @classmethod
    def _check_container_init(cls) -> None:
        if cls.container is None:
            raise RuntimeError("Inject context container has not been initialized")

        if not isinstance(cls.container, (AsyncContainer, Container)):
            raise TypeError(
                f"{cls.container} is {cls.container.__class__.__name__}, "
                "not Container or AsyncContainer"
            )

    @classmethod
    def inject(cls, func: t.Callable[P, T]) -> t.Callable[P, T]:
        if not iscoroutinefunction(func):
            raise AttributeError(
                f"Function `{func.__name__}` is not async function. "
                f"For sync functions, use `@sync_inject` decorator instead."
            )

        @wraps(func)
        async def wrapper(*args, **kwargs):
            cls._check_container_init()

            async with cls.container() as request_container:
                wrapped = wrap_injection(
                    func=func,
                    remove_depends=True,
                    container_getter=lambda _, __: request_container,
                    is_async=True,
                )
                return await wrapped(*args, **kwargs)

        return wrapper

    @classmethod
    def sync_inject(cls, func: t.Callable[P, T]) -> t.Callable[P, T]:
        if iscoroutinefunction(func):
            raise AttributeError(
                f"Function `{func.__name__}` is async function. "
                f"For async functions, use `@inject` decorator instead."
            )

        @wraps(func)
        def wrapper(*args, **kwargs):
            cls._check_container_init()

            with cls.container() as request_container:
                wrapped = wrap_injection(
                    func=func,
                    remove_depends=True,
                    container_getter=lambda _, __: request_container,
                    is_async=False,
                )
                return wrapped(*args, **kwargs)

        return wrapper
