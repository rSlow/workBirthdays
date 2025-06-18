from abc import ABC

from aiogram_dialog import ShowMode


class UserNotifyException(Exception, ABC):
    """
    Базовый класс исключения для отправки сообщения пользователю.
    """

    message_text: str = "Оповещение"
    show_mode: ShowMode = ShowMode.DELETE_AND_SEND

    def __init__(self, **kwargs):
        self.map_kwargs = kwargs

    @property
    def message(self):
        return self.message_text.format_map(self.map_kwargs)
