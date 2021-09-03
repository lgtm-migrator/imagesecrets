"""Application Programming Interface."""
from __future__ import annotations

import imagesecrets
from fastapi import Depends, FastAPI, status
from imagesecrets.api import (
    dependencies,
    handlers,
    openapi,
    responses,
    schemas,
    tasks,
)
from imagesecrets.api.routers import decode, encode, user
from imagesecrets.config import Settings, settings
from imagesecrets.database import base


def create_api(config: Settings) -> FastAPI:
    api = FastAPI(
        dependencies=[Depends(dependencies.get_config)],
        title="ImageSecrets",
        description="Encode and decode messages from images!",
        version=imagesecrets.__version__,
        # will be set manually
        docs_url=None,
        redoc_url=None,
        responses=responses.VALIDATION,  # type: ignore
    )

    # tortoise setup
    base.init(api)

    api.include_router(decode.router)
    api.include_router(encode.router)
    api.include_router(user.main)
    api.include_router(user.me)

    handlers.init(api)
    tasks.init(api)

    @api.get(
        "/",
        response_model=schemas.Info,
        status_code=status.HTTP_200_OK,
        summary="Basic information about the API.",
        tags=["home"],
    )
    async def home(
        settings: Settings = Depends(dependencies.get_config),
    ) -> dict[str, str]:
        """Return basic info about the API."""
        return {
            "AppName": settings.app_name,
            "SwaggerUI": settings.swagger_url,
            "ReDoc": settings.redoc_url,
            "GitHub": settings.repository_url,
        }

    api.openapi = openapi.custom(api, swagger=True, redoc=True)  # type: ignore

    return api


def create_application():
    """Create the application."""
    return create_api(settings)


app = create_application()


__all__ = ["app", "create_application", "create_api"]
