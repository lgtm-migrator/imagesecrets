"""Application Programming Interface"""
import shutil

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from image_secrets.api import config, exceptions
from image_secrets.api.dependencies import get_settings
from image_secrets.api.routers import decode, encode, user
from image_secrets.settings import API_IMAGES

app = FastAPI(
    dependencies=[Depends(get_settings)],
    title="ImageSecrets",
    description="Encode and decode messages from images!",
    version="0.1.0",
)
app.include_router(user.router)
app.include_router(decode.router)
app.include_router(encode.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = exc.errors()[0]
    msg = errors["msg"]
    field = errors["loc"][-1]
    return await exceptions.handler(status_code=422, message=msg, field=field)


@app.exception_handler(exceptions.DetailExists)
async def http_exception_handler(
    request: Request,
    exc: exceptions.DetailExists,
) -> JSONResponse:
    return await exceptions.handler(
        status_code=exc.status_code,
        message=exc.message,
        field=exc.field,
    )


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
