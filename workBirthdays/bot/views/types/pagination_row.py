from aiogram_dialog.widgets.common import WhenCondition, Scroll
from aiogram_dialog.widgets.kbd import Row, Keyboard, PrevPage, CurrentPage, NextPage
from aiogram_dialog.widgets.text import Text, Const, Format


class PaginationRow(Row):
    def __init__(
            self,
            id_: str,
            scroll: str | Scroll,
            prev_text: Text = Const("◀️"),
            current_text: Text = Format("{current_page1} / {pages}"),
            next_text: Text = Const("▶️"),
            when: WhenCondition = None,
    ):
        self._scroll = scroll
        self._scroll_name = self._get_scroll_name()

        self._prev_text = prev_text
        self._current_text = current_text
        self._next_text = next_text

        super().__init__(*self._get_row_buttons(), id=id_, when=when)

    def _get_scroll_name(self) -> str:
        return getattr(self._scroll, "widget_id", str(self._scroll))

    def _get_row_buttons(self) -> list[Keyboard]:
        return [
            PrevPage(
                id=self._scroll_name + "_prev",
                scroll=self._scroll, text=self._prev_text
            ),
            CurrentPage(
                id=self._scroll_name + "_current", scroll=self._scroll,
                text=self._current_text
            ),
            NextPage(
                id=self._scroll_name + "_next",
                scroll=self._scroll, text=self._next_text
            ),
        ]
