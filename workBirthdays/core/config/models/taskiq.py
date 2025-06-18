from dataclasses import dataclass

from .redis import RedisConfig


@dataclass
class ResultBackendConfig(RedisConfig):
    pass


@dataclass
class MQConfig:
    host: str
    user: str
    password: str
    port: int | None = None
    backend: ResultBackendConfig | None = None

    @property
    def uri(self):
        url = f"amqp://{self.user}:{self.password}@{self.host}"
        if self.port:
            url += f":{self.port}"
        return url
