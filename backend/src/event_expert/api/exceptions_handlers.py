"""
API Exception Handlers
======================

Global exception handlers for the
Event Expert System REST API.

Responsibilities
----------------
- Translate domain exceptions into HTTP responses
- Provide consistent API error responses
- Hide internal implementation details
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from ..modules.knowledge.exceptions import (
    ForwardChainingError,
    KnowledgeBaseNotInitializedError,
    RepositoryLoadingError,
    RepositoryValidationError,
)


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register all API exception handlers.
    """

    # ======================================================
    # Repository Loading
    # ======================================================

    @app.exception_handler(
        RepositoryLoadingError
    )
    async def repository_loading_handler(
        request: Request,
        exc: RepositoryLoadingError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "RepositoryLoadingError",
                "message": str(exc),
            },
        )

    # ======================================================
    # Repository Validation
    # ======================================================

    @app.exception_handler(
        RepositoryValidationError
    )
    async def repository_validation_handler(
        request: Request,
        exc: RepositoryValidationError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "RepositoryValidationError",
                "message": str(exc),
            },
        )

    # ======================================================
    # Knowledge Cache
    # ======================================================

    @app.exception_handler(
        KnowledgeBaseNotInitializedError
    )
    async def knowledge_base_not_initialized_handler(
        request: Request,
        exc: KnowledgeBaseNotInitializedError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "KnowledgeBaseNotInitializedError",
                "message": str(exc),
            },
        )

    # ======================================================
    # Forward Chaining
    # ======================================================

    @app.exception_handler(
        ForwardChainingError
    )
    async def forward_chaining_handler(
        request: Request,
        exc: ForwardChainingError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "ForwardChainingError",
                "message": str(exc),
            },
        )

    # ======================================================
    # Fallback
    # ======================================================

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": type(exc).__name__,
                "message": "An unexpected internal server error occurred.",
            },
        )