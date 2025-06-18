from abc import ABC


class BaseError(Exception, ABC):
    """
    Базовый класс ошибки для ее логирования.
    Опционально: вывод сообщения пользователю.
    Опционально: отключение логирования, только для
                 отправки сообщения пользователю.
    """

    log: bool = True
    log_message: str = "Ошибка"
    user_note_template: str | None = None

    def __init__(
            self,
            user_id: int | None = None,
            chat_id: int | None = None,
            **kwargs
    ):
        self.user_id = user_id
        self.chat_id = chat_id
        self.map_kwargs = kwargs

    def __repr__(self) -> str:
        result_msg = self.log_message
        if self.user_id is not None:
            result_msg += f", у пользователя {self.user_id}"
        if self.chat_id is not None:
            result_msg += f", в чате {self.chat_id}"
        return result_msg.format_map(self.map_kwargs)

    __str__ = __repr__

    @property
    def note_for_user(self):
        if self.user_note_template is not None:
            return self.user_note_template.format_map(self.map_kwargs)
        return "Внимание: текст оповещения не установлен!"
