from typing import Callable, Awaitable

from aiogram import types
from aiogram_dialog import DialogManager

OnFinish = Callable[[types.Message, DialogManager], Awaitable[None]]
