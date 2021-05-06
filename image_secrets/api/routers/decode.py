"""Decode router."""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from image_secrets.api import config
from image_secrets.api.dependencies import get_settings
from image_secrets.backend.decode import decode_text
from image_secrets.backend.util import image_data

router = APIRouter(
    tags=["decode"],
    dependencies=[Depends(get_settings)],
)


@router.get("/decode/")
async def encode_home(settings: config.Settings = Depends(get_settings)) -> dict:
    return {"app-name": settings.app_name}


@router.post("/decode")
async def decode(file: UploadFile = File(...)) -> dict[str:str, str:str]:
    """Decode a message from the given file.

    :param file: The uploaded file

    """
    _, arr = image_data(file.file)

    try:
        return {"file": file.filename, "message": decode_text(arr)}
    except StopIteration as e:
        raise HTTPException(status_code=400, detail=e.args) from e
