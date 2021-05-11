"""Application Programming Interface"""
import shutil

from fastapi import Depends, FastAPI

from image_secrets.api import config
from image_secrets.api.dependencies import get_settings
from image_secrets.api.routers import decode, encode
from image_secrets.settings import API_IMAGES

app = FastAPI(
    dependencies=[Depends(get_settings)],
    title="ImageSecrets",
    description="Encode and decode messages from images!",
    version="0.1.0",
    redoc_url=None,
)
app.include_router(decode.router)
app.include_router(encode.router)


@app.on_event("startup")
async def startup() -> None:
    """Startup event."""
    API_IMAGES.mkdir(parents=True, exist_ok=True)


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown event."""
    shutil.rmtree(API_IMAGES)
    API_IMAGES.unlink(missing_ok=True)


@app.get(
    "/",
    response_model=dict[str, str],
    summary="Basic information about the API.",
    tags=["home"],
)
async def home(settings: config.Settings = Depends(get_settings)) -> dict[str, str]:
    """Return basic info about the home route."""
    return {"app-name": settings.app_name}


__all__ = [
    "app",
    "home",
    "shutdown",
    "startup",
]
