from datetime import date

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarScopeView, CalendarDaysView, CalendarMonthView, CalendarYearsView
)
from aiogram_dialog.widgets.text import Text
from babel.dates import get_day_names, get_month_names


class LocalizedWeekDay(Text):
    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        weekdays = get_day_names(
            width='short',
            context='stand-alone',
            locale=locale
        )
        weekday = weekdays[selected_date.weekday()]
        return weekday.title()


class LocalizedMonth(Text):
    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        months = get_month_names(
            width='wide',
            context='stand-alone',
            locale=locale
        )
        month = months[selected_date.month]
        return month.title()


class LocalizedCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                header_text="🗓 " + LocalizedMonth(),
                weekday_text=LocalizedWeekDay(),
                next_month_text=LocalizedMonth() + " >>",
                prev_month_text="<< " + LocalizedMonth(),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=LocalizedMonth(),
                this_month_text="[" + LocalizedMonth() + "]",
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
            ),
        }
