"""Custom OpenAPI schema."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from fastapi.openapi import docs, utils

import image_secrets

if TYPE_CHECKING:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse


def custom(app: FastAPI) -> Callable[[], dict[str, Any]]:
    """Return custom OpenAPI generation function."""

    @app.get("/docs", include_in_schema=False)
    def override_swagger() -> HTMLResponse:
        """Override Swagger UI."""
        return docs.get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="ImageSecrets",
            swagger_favicon_url="...",
        )

    @app.get("/redoc", include_in_schema=False)
    def override_redoc() -> HTMLResponse:
        """Override ReDoc."""
        return docs.get_redoc_html(
            openapi_url="/openapi.json",
            title="ImageSecrets",
            redoc_favicon_url="...",
        )

    def schema() -> dict[str, Any]:
        """Return custom OpenAPI schema."""
        nonlocal app

        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = utils.get_openapi(
            title="ImageSecrets",
            version=image_secrets.__version__,
            description="Encode and decode messages from images!",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return schema
