from typing import Optional, Any, Callable, TypeVar

from aiogram import types
from aiogram.fsm.state import State
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input.text import (
    OnSuccess, OnError, ManagedTextInput
)
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.kbd.select import TypeFactory
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.utils import GetterVariant

T = TypeVar("T")


class InputFormField(State):
    def __init__(
            self,
            *texts: Text,
            keyboard: Optional[Keyboard] = None,
            type_factory: TypeFactory[T] = str,
            on_success: Optional[OnSuccess[T]] = None,
            on_error: Optional[OnError] = None,
            error_message: str | None = None,
            filter_: Optional[Callable[..., Any]] = None,
            show_current_value: bool = True,
            current_value_text: Optional[Text] = None,
            getter: GetterVariant = None,
            state: Optional[str] = None,
            group_name: Optional[str] = None
    ):
        super().__init__(state, group_name)

        self.texts = texts
        self.keyboard = keyboard
        self.type_factory = type_factory
        self._on_success = on_success
        self._on_error = on_error
        self.error_message = error_message
        self.filter = filter_
        self.show_current_value = show_current_value
        self.current_value_text_widget = current_value_text
        self.getter = getter

    @property
    def on_success(self):
        if self._on_success is None:
            return self._default_on_success
        return self._on_success

    @property
    def on_error(self):
        if self._on_error is None:
            return self._default_on_error
        return self._on_success

    @property
    def field_name(self):
        return self.state.split(":")[-1]

    @staticmethod
    async def _default_on_success(
            _, text_input: ManagedTextInput, manager: DialogManager, text: str
    ):
        widget_id = text_input.widget.widget_id
        manager.dialog_data.update({widget_id: text})
        try:
            await manager.next()
        except IndexError:
            pass

    async def _default_on_error(
            self, message: types.Message, _widget: ManagedTextInput[str], manager: DialogManager,
            error: ValueError
    ):
        manager.show_mode = ShowMode.DELETE_AND_SEND
        if self.error_message is not None:
            await message.answer(
                self.error_message.format_map({"error": error, "message": message})
            )

    def copy(self):
        return InputFormField(
            *self.texts,
            state=self._state,
            group_name=self._group_name,
            keyboard=self.keyboard,
            type_factory=self.type_factory,
            on_success=self._on_success,
            on_error=self._on_error,
            filter_=self.filter,
            show_current_value=self.show_current_value,
            current_value_text=self.current_value_text_widget,
            getter=self.getter
        )
