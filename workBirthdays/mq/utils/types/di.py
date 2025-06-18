from typing import Callable, Awaitable

from taskiq import TaskiqMessage
from taskiq.result.v2 import TaskiqResult

ExceptionHandler = Callable[
    [BaseException, TaskiqMessage, TaskiqResult],
    Awaitable[None]
]
