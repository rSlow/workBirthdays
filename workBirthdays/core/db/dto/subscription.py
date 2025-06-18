from dataclasses import dataclass


@dataclass
class Subscription:
    url: str
    name: str
    user_id: int
    frequency: int
    is_active: bool | None = None

    id_: int | None = None
