"""Application Programming Interface."""
from __future__ import annotations

from fastapi import Depends, FastAPI, status

from image_secrets.api import config, dependencies, handlers, responses
from image_secrets.api.routers import decode, encode, users
from image_secrets.backend.database import base

config_ = dependencies.get_config()
app = FastAPI(
    dependencies=[Depends(dependencies.get_config)],
    title="ImageSecrets",
    description="Encode and decode messages from images!",
    version="0.2.0",
    responses=responses.VALIDATION,
)

# tortoise setup
base.init(app, config_.pg_dsn)

app.include_router(decode.router)
app.include_router(encode.router)
app.include_router(users.main)
app.include_router(users.me)

handlers.init(app)


@app.get(
    "/",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Basic information about the API.",
    tags=["home"],
)
async def home(
    settings: config.Settings = Depends(dependencies.get_config),
) -> dict[str, str]:
    """Return basic info about the home route."""
    return {"app-name": settings.app_name}


__all__ = [
    "app",
    "home",
]
