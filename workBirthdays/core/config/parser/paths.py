from pathlib import Path

from ..models.paths import Paths


def get_paths() -> Paths:
    return Paths(Path(__file__).parent.parent.parent.parent.parent)
