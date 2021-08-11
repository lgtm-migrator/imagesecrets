"""Application Programming Interface."""
from __future__ import annotations

from fastapi import Depends, FastAPI, status

import image_secrets
from image_secrets.api import (
    config,
    dependencies,
    handlers,
    openapi,
    responses,
    schemas,
    tasks,
)
from image_secrets.api.routers import decode, encode, user
from image_secrets.backend.database import base

config_ = dependencies.get_config()
app = FastAPI(
    dependencies=[Depends(dependencies.get_config)],
    title="ImageSecrets",
    description="Encode and decode messages from images!",
    version=image_secrets.__version__,
    # will be set manually
    docs_url=None,
    redoc_url=None,
    responses=responses.VALIDATION,  # type: ignore
)

# tortoise setup
base.init(app, config_.pg_dsn)

app.include_router(decode.router)
app.include_router(encode.router)
app.include_router(user.main)
app.include_router(user.me)

handlers.init(app)
tasks.init(app)


@app.get(
    "/",
    response_model=schemas.Info,
    status_code=status.HTTP_200_OK,
    summary="Basic information about the API.",
    tags=["home"],
)
async def home(
    settings: config.Settings = Depends(dependencies.get_config),
) -> dict[str, str]:
    """Return basic info about the API."""
    return {
        "AppName": settings.app_name,
        "SwaggerUI": settings.swagger_url,
        "ReDoc": settings.redoc_url,
        "GitHub": settings.repository_url,
    }


app.openapi = openapi.custom(app, swagger=True, redoc=True)  # type: ignore


__all__ = [
    "app",
    "home",
]
