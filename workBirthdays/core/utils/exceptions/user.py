from .base import BaseError


class UnknownUserError(BaseError):
    log_message = "Пользователь не найден."


class UnknownUserIdError(UnknownUserError):
    log = False
    user_note_template = "Unknown user ID: {user_id}"


class UnknownUsernameFound(UnknownUserError):
    log_message = "По имени пользователя {username} пользователь не найден."


class UnknownUserTgIdError(UnknownUserError):
    log_message = "По Telegram ID {tg_id} пользователь не найден."


class MultipleUsernameFound(BaseError):
    log_message = "По имени пользователя {username} найдено несколько пользователей."
