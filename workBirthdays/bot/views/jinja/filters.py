from datetime import datetime, timedelta

from workBirthdays.core.utils import dates


def datetime_filter(
        value: datetime | None, format_: str = dates.DATETIME_FORMAT
) -> str:
    if value is None:
        return "n/a"
    return value.strftime(format_)


def timedelta_filter(value: timedelta) -> str:
    minutes = value.seconds // 60
    return f"{minutes} мин."
