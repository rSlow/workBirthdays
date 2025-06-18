from abc import abstractmethod
from typing import Protocol

from aiogram_dialog import DialogManager


class DialogGetter(Protocol):
    @abstractmethod
    async def __call__(self, **kwargs) -> dict:
        ...


class DialogDataGetter(DialogGetter):
    async def __call__(self, dialog_manager: DialogManager, **kwargs):
        return dialog_manager.dialog_data
