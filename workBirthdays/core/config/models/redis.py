from dataclasses import dataclass


@dataclass
class RedisConfig:
    host: str
    password: str
    db: int
    port: int | None = None

    @property
    def uri(self):
        url = f"redis://:{self.password}@"
        if self.host:
            url += self.host
        if self.port:
            url += f":{self.port}"
        url += f"/{self.db}"
        return url
