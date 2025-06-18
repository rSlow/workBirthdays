from dataclasses import dataclass
from typing import Optional

from aiogram.types import UNSET_PARSE_MODE
from aiogram.types.base import UNSET_DISABLE_WEB_PAGE_PREVIEW
from aiogram_dialog.api.internal.widgets import MarkupFactory
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.markup.inline_keyboard import InlineKeyboardFactory
from aiogram_dialog.widgets.utils import GetterVariant


@dataclass
class WindowTemplate:
    markup_factory: MarkupFactory = InlineKeyboardFactory()
    parse_mode: Optional[str] = UNSET_PARSE_MODE
    disable_web_page_preview: bool | None = UNSET_DISABLE_WEB_PAGE_PREVIEW
    preview_add_transitions: Optional[list[Keyboard]] = None
    preview_data: GetterVariant = None
    add_main_menu_button: bool = False
