from dataclasses import dataclass
from datetime import date as d
from uuid import UUID

from workBirthdays.core.utils.dates import get_now


@dataclass
class Birthday:
    uuid: UUID
    fio: str
    date: d
    post: str | None = None
    rank: str | None = None

    @property
    def age(self):
        return int(round((get_now().date() - self.date).days / 362.25))

    @property
    def declension(self):
        age = self.age
        if age % 10 == 1 and age != 11:
            return "год"
        elif age % 10 in [2, 3, 4] and (age < 10 or age > 20):
            return "года"
        return "лет"
