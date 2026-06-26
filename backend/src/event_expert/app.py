from fastapi import FastAPI

from .infrastructure.config.settings import settings

from .api.routers.health import router as health_router
from .api.routers.system import router as system_router


def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.include_router(system_router)
    app.include_router(health_router)

    return app