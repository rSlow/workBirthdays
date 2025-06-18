from .base import BaseError


class TaskiqTaskError(BaseError):
    log_message = "Ошибка выполнения задачи: {message}: {error}"

    def __init__(
            self, message: str, error: BaseException,
            user_message: str | None = None
    ):
        super().__init__()
        self.map_kwargs = {
            "message": message,
            "error": repr(error)
        }
        self.user_note_template = user_message
