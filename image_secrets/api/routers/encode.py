"""API routers."""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from image_secrets.api import config
from image_secrets.api.dependencies import get_settings
from image_secrets.backend.encode import api_encode
from image_secrets.backend.util import save_image
from image_secrets.settings import MESSAGE_DELIMETER

router = APIRouter(
    tags=["encode"],
    dependencies=[Depends(get_settings)],
)


@router.get("/encode/")
async def encode_home(settings: config.Settings = Depends(get_settings)) -> dict:
    return {"app-name": settings.app_name}


@router.post("/encode/")
async def encode(
    message: str,
    file: UploadFile = File(...),
    custom_delimeter: str = MESSAGE_DELIMETER,
    lsb_n: int = 1,
    reverse: bool = False,
) -> FileResponse:
    """Encode a message into the source image.

    :param message: Message to encode
    :param file: Source image

    """
    try:
        data = api_encode(message, file, custom_delimeter, lsb_n, reverse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args) from e

    fp = config.settings.image_folder / file.filename
    save_image(data, fp)
    try:
        return FileResponse(fp)
    finally:
        fp.unlink()
