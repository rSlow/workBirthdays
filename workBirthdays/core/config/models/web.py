from dataclasses import dataclass


@dataclass
class WebConfig:
    base_url: str
    root_path: str | None = None

    @property
    def real_base_url(self) -> str:
        if self.root_path:
            return self.base_url + self.root_path
        return self.base_url
