"""Application Programming Interface"""
import shutil
from pathlib import Path

from fastapi import Depends, FastAPI

from image_secrets.api import config
from image_secrets.api.dependencies import get_settings
from image_secrets.api.routers import decode, encode

app = FastAPI(dependencies=[Depends(get_settings)])
app.include_router(decode.router)
app.include_router(encode.router)


@app.on_event("startup")
async def startup() -> None:
    """Startup event."""
    images = Path(f"images/").absolute()
    images.mkdir(exist_ok=True)


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown event."""
    images = Path(f"images/").absolute()
    shutil.rmtree(images)
    images.unlink(missing_ok=True)


@app.get("/")
@app.get("/home")
async def home(settings: config.Settings = Depends(get_settings)) -> dict:
    """Return basic info about the home route."""
    return {"app-name": settings.app_name}
