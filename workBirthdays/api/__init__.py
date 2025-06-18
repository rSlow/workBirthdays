import logging

from asgi_monitor.integrations.fastapi import setup_metrics, MetricsConfig
from fastapi import FastAPI

from workBirthdays.api import routes
from workBirthdays.api.config.models import ApiAppConfig

logger = logging.getLogger(__name__)


def create_app(config: ApiAppConfig) -> FastAPI:
    app = FastAPI(
        root_path=config.api.root_path_with_base(config.web.root_path)
    )
    routes.setup(app)
    # middlewares.setup(app, config)
    setup_metrics(
        app,
        MetricsConfig(
            app_name=config.app.name,
            include_metrics_endpoint=True,
            include_trace_exemplar=True,
        ),
    )

    return app
