from typing import Optional

from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd.checkbox import Checkbox, OnStateChanged
from aiogram_dialog.widgets.text import Text


class DataCheckbox(Checkbox):
    def __init__(
            self, checked_text: Text, unchecked_text: Text, id: str,
            data_getter: str, default: bool = False,
            on_state_changed: Optional[OnStateChanged] = None, when: WhenCondition = None
    ):
        super().__init__(
            checked_text=checked_text, unchecked_text=unchecked_text, id=id,
            default=default, on_state_changed=on_state_changed, when=when,
        )
        self._data_getter = data_getter

    def is_checked(self, manager: DialogManager) -> bool:
        if (value := manager.dialog_data.get(self._data_getter)) is not None:
            return bool(value)
        return super().is_checked(manager)

    async def set_checked(self, event: ChatEvent, checked: bool, manager: DialogManager) -> None:
        manager.dialog_data[self._data_getter] = checked
        await self.on_state_changed.process_event(event, self.managed(manager), manager)
