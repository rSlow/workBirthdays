from workBirthdays.core.utils.exceptions import BaseError


class BigDurationError(BaseError):
    log_message = (
        "Видео, на которое вы отправили ссылку, идет более 10 минут. "
        "По техническим причинам на данный момент скачивание аудио "
        "более 10 минут невозможно."
    )
