from aiogram import types as t

from workBirthdays.core.utils.exceptions.base import BaseError


class EventTypeError(BaseError):
    log_message = "Ошибка типа события: {event_name}"

    def __init__(self, event: t.TelegramObject, **kwargs):
        super().__init__(event_name=event.__class__.__name__, **kwargs)


class UnknownEventTypeError(EventTypeError):
    log_message = "Неподдерживаемый тип события: {event_name}"


class PassEventException(EventTypeError):
    log_message = "Тип события {event_name} исключен из обработки."
