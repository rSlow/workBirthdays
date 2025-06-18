import re
from re import Pattern

HTTPS_REGEXP = (
    r"https?:\/\/"
    r"(www\.)?"
    r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\."
    r"[a-zA-Z0-9()]{1,6}"
    r"\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)
TIMECODE_REGEXP = r"^(\d{2}:)?\d{2}:\d{2}$"
PAIR_TIMECODE_REGEXP = TIMECODE_REGEXP[:-1] + r"-" + TIMECODE_REGEXP[1:]


def regexp_factory(pattern: str | Pattern[str]):
    def _factory(value: str):
        res = re.match(pattern, value)
        if res is None:
            raise ValueError
        return value

    return _factory
