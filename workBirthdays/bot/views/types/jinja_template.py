import typing as t
from typing import Optional

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

from workBirthdays.bot.middlewares.config import MiddlewareData


class JinjaTemplate(Text):
    def __init__(
            self, template_path: str,
            template_data: Optional[dict] = None, when: WhenCondition = None
    ):
        super().__init__(when=when)
        self._template_path = template_path
        if template_data is None:
            self._template_data = {}
        else:
            self._template_data = template_data.copy()

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        middleware_data = t.cast(MiddlewareData, manager.middleware_data)
        renderer = middleware_data["jinja_renderer"]
        self._template_data.update(data)
        return renderer.render_template(
            template_path=self._template_path,
            context=self._template_data
        )
