from workBirthdays.core.utils.exceptions.base import BaseError


class UnknownContentTypeError(BaseError):
    log_message = "Неизвестный тип контента: {file_content_type}"
