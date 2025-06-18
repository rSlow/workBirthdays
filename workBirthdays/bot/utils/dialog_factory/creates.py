from typing import Optional, Any

from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Cancel, Back, Next
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Const, Text


def _create_cancel_button(
        text: Text = Const("Назад ◀"), result: Any | None = None,
        on_click: Optional[OnClick] = None, when: WhenCondition = None
):
    return Cancel(text=text, id="__cancel__", result=result, on_click=on_click, when=when)


def _create_back_button(
        text: Text = Const("Назад ◀"), on_click: Optional[OnClick] = None,
        when: WhenCondition = None
):
    return Back(text=text, id="__back__", on_click=on_click, when=when)


def _create_next_button(
        text: Text = Const("Вперед ▶"), on_click: Optional[OnClick] = None,
        when: WhenCondition = None
):
    return Next(text=text, id="__next__", on_click=on_click, when=when)
