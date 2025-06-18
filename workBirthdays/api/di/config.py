from dishka import Provider, Scope, provide, from_context

from workBirthdays.api.config.models import ApiAppConfig
from workBirthdays.api.config.models.api import ApiConfig


class ApiProvider(Provider):
    scope = Scope.APP

    api_config = from_context(ApiAppConfig)

    @provide
    def get_api_config(self, api_app: ApiAppConfig) -> ApiConfig:
        return api_app.api
