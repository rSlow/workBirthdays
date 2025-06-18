from dataclasses import dataclass


@dataclass
class WebhookConfig:
    path: str
    secret: str
