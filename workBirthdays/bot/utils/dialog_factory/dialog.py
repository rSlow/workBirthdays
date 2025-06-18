from functools import wraps
from typing import Optional

from aiogram import types
from aiogram_dialog import Dialog, Window, LaunchMode, DialogManager
from aiogram_dialog.dialog import OnResultEvent, OnDialogEvent
from aiogram_dialog.widgets.input.text import OnSuccess, TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Row
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.utils import GetterVariant

from workBirthdays.bot.views import buttons as b
from .creates import _create_cancel_button, _create_next_button, _create_back_button
from .form import InputForm
from .getters import DialogDataGetter
from .types import OnFinish
from .window import WindowTemplate


class InputDialogFactory:
    def __init__(
            self,
            input_form: type[InputForm],
            on_finish: OnFinish,
            template: WindowTemplate = WindowTemplate
    ):
        self.input_form = input_form
        self.on_finish = on_finish
        self.template = template

    def _with_last_field_handler(self, on_success: OnSuccess) -> OnSuccess:
        @wraps(self.on_finish)
        async def _on_success(
                message: types.Message, text_input: ManagedTextInput, manager: DialogManager,
                text: str
        ):
            await on_success(message, text_input, manager, text)
            await self.on_finish(message, manager)

        return _on_success

    def dialog(
            self,
            on_start: Optional[OnDialogEvent] = None,
            on_close: Optional[OnDialogEvent] = None,
            on_process_result: Optional[OnResultEvent] = None,
            launch_mode: LaunchMode = LaunchMode.STANDARD,
            getter: GetterVariant = None,
            preview_data: GetterVariant = None,
            name: Optional[str] = None
    ):
        windows = []

        for form_field in self.input_form.get_fields():
            field_name = form_field.field_name
            widgets = [*form_field.texts]

            if form_field == self.input_form.last():
                _on_success = self._with_last_field_handler(form_field.on_success)
            else:
                _on_success = form_field.on_success

            widgets.append(
                TextInput(
                    id=field_name,
                    type_factory=form_field.type_factory,
                    on_success=_on_success,
                    on_error=form_field.on_error,
                    filter=form_field.filter
                )
            )

            if form_field.show_current_value:
                if form_field.current_value_text_widget is None:
                    form_field.current_value_text_widget = Format(
                        "\nТекущее значение - <i>{" + field_name + "}</i>",
                        when=field_name
                    )
                widgets.append(form_field.current_value_text_widget)

            if form_field.keyboard is not None:
                widgets.append(form_field.keyboard)

            if form_field == self.input_form.first():
                widgets.append(
                    Row(
                        _create_cancel_button(),
                        _create_next_button(when=form_field.field_name)
                    )
                )
            elif form_field == self.input_form.last():
                widgets.append(_create_back_button())
            else:
                widgets.append(
                    Row(
                        _create_back_button(),
                        _create_next_button(when=form_field.field_name)
                    )
                )

            if self.template.add_main_menu_button:
                widgets.append(b.MAIN_MENU)

            window = Window(
                *widgets,
                getter=form_field.getter,
                markup_factory=self.template.markup_factory,
                parse_mode=self.template.parse_mode,
                disable_web_page_preview=self.template.disable_web_page_preview,
                preview_add_transitions=self.template.preview_add_transitions,
                preview_data=self.template.preview_data,
                state=form_field,
            )
            windows.append(window)

        if getter is None:
            _getter = DialogDataGetter()
        elif isinstance(getter, (tuple, list)):
            _getter = [*getter, DialogDataGetter()]
        else:
            raise TypeError("getter is not `GetterVariant`")

        return Dialog(
            *windows,
            on_start=on_start,
            on_close=on_close,
            on_process_result=on_process_result,
            launch_mode=launch_mode,
            getter=_getter,
            preview_data=preview_data,
            name=name,
        )
