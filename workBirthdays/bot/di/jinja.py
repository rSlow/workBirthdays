import logging

from dishka import Provider, provide, Scope
from jinja2 import Environment, FileSystemLoader, BaseLoader, Template

from workBirthdays.bot.views import jinja
from workBirthdays.bot.views.jinja.filters import datetime_filter, timedelta_filter
from workBirthdays.core.config import Paths
from workBirthdays.core.utils import dates
from workBirthdays.core.utils.dates import get_now

logger = logging.getLogger(__name__)


class JinjaRenderer:
    def __init__(self, environment: Environment):
        self.environment = environment

    def render_template(
            self, template_path: str | Template, context: dict | None = None,
            **kwargs
    ):
        _context = (context or {}) | kwargs
        _context.update({
            "now": get_now(),
            "TIME_FORMAT_USER": dates.TIME_FORMAT_USER,
            "DATE_FORMAT_USER": dates.DATE_FORMAT_USER,
            "DATETIME_FORMAT_USER": dates.DATETIME_FORMAT_USER
        })
        template = self.environment.get_template(template_path)
        return jinja.render_template(template, _context)


class JinjaProvider(Provider):
    scope = Scope.APP

    renderer = provide(JinjaRenderer)

    @provide
    def get_environment(self, loader: BaseLoader) -> Environment:
        filters = {
            "datetime": datetime_filter,
            "time": lambda x: datetime_filter(x, dates.TIME_FORMAT),
            "date": lambda x: datetime_filter(x, dates.DATE_FORMAT),
            "timedelta": timedelta_filter,
        }
        env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True, autoescape=True)
        env.filters.update(filters)
        logger.info(f"Jinja init with loader <{loader.__class__.__name__}>")
        return env

    @provide
    def get_loader(self, paths: Paths) -> BaseLoader:
        return FileSystemLoader(searchpath=paths.bot_path / "views" / "jinja" / "templates")
