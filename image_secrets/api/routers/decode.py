"""Decode router."""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from image_secrets.api import config
from image_secrets.api.dependencies import get_settings
from image_secrets.backend import decode as b_decode
from image_secrets.backend.util import image_data

router = APIRouter(
    tags=["decode"],
    dependencies=[Depends(get_settings)],
)


@router.get("/decode/")
async def decode_home(settings: config.Settings = Depends(get_settings)) -> dict:
    return {"app-name": settings.app_name}


@router.post("/decode")
async def decode(file: UploadFile = File(...)) -> dict[str:str, str:str]:
    """Decode a message from the given file.

    :param file: The uploaded file

    """
    data = await file.read()
    try:
        return {
            "file": file.filename,
            "message": b_decode.api(data, "<{~stop-here~}>", 1, False),
        }
    except StopIteration as e:
        raise HTTPException(status_code=400, detail=e.args) from e


__all__ = ["decode", "decode_home", "router"]
