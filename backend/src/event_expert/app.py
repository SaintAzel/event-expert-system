from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .infrastructure.config.settings import settings

from .api.routers.health import router as health_router
from .api.routers.system import router as system_router
from .api.routers.evaluation import router as evaluation_router
from .api.exceptions_handlers import (
    register_exception_handlers,
)

def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:4173",
            "http://localhost:4173",
            "http://127.0.0.1:5500",
            "http://localhost:5500",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(system_router)

    app.include_router(health_router)

    app.include_router(evaluation_router)

    register_exception_handlers(app)

    return app
