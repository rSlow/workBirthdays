from aiogram.fsm.state import State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Cancel, SwitchTo
from aiogram_dialog.widgets.kbd.button import OnClick, Button
from aiogram_dialog.widgets.text import Text, Const
from aiogram_dialog.widgets.utils import GetterVariant


def choice_dialog_factory(
        *texts: Text, state: State, on_click: OnClick, getter: GetterVariant = None
):
    return Dialog(
        Window(
            *texts,
            Row(
                Button(
                    Const("Да"),
                    on_click=on_click,
                    id="yes"
                ),
                Cancel(Const("Нет"))
            ),
            state=state,
            getter=getter,
        )
    )


def choice_window_factory(
        *texts: Text, state: State, on_click: OnClick, back_state: State,
        getter: GetterVariant = None
):
    return Window(
        *texts,
        Row(
            Button(
                Const("Да"),
                on_click=on_click,
                id="yes"
            ),
            SwitchTo(
                Const("Нет"),
                id="no",
                state=back_state
            )
        ),
        getter=getter,
        state=state
    )
