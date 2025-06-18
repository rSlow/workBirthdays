from dishka import Provider, provide, Scope

from workBirthdays.core.config.models import (
    Paths, BaseConfig, WebConfig, MQConfig, SecurityConfig, AppConfig,
)


class BaseConfigProvider(Provider):
    scope = Scope.APP

    def __init__(self, config: BaseConfig):
        super().__init__()
        self.base_config = config.as_base()

    @provide
    def get_base_config(self) -> BaseConfig:
        return self.base_config

    @provide
    def get_paths(self, config: BaseConfig) -> Paths:
        return config.paths

    @provide
    def get_web_config(self, config: BaseConfig) -> WebConfig:
        return config.web

    @provide
    def get_mq_config(self, config: BaseConfig) -> MQConfig:
        return config.mq

    @provide
    def get_auth_config(self, config: BaseConfig) -> SecurityConfig:
        return config.auth

    @provide
    def get_app_config(self, config: BaseConfig) -> AppConfig:
        return config.app
