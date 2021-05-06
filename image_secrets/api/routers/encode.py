"""API routers."""

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
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


@router.get(
    "/encode/",
    response_model=dict[str, str],
    summary="Information about the encode route",
)
async def encode_home(settings: config.Settings = Depends(get_settings)) -> dict:
    return {"app-name": settings.app_name}


@router.post("/encode/", summary="Encode a message into an image")
async def encode_message(
    settings: config.Settings = Depends(get_settings),
    *,
    message: str = Query(
        ...,
        title="message to encode",
        description="The message to encode into the image.",
    ),
    file: UploadFile = File(
        ...,
        description="The image in which to encode the message.",
    ),
    delim: str = Query(
        MESSAGE_DELIMETER,
        description="""String which is going to be appended to the end of your message
        so that the message can be decoded later.""",
        alias="custom-delimeter",
    ),
    lsb_n: int = Query(
        1,
        title="Number of least significant bits to alter.",
        ge=1,
        le=8,
        alias="least-significant-bit-amount",
    ),
    rev: bool = Query(
        False,
        alias="reversed-encoding",
        description="Message will be encoded starting from the last pixel instead of the first one.",
    ),
) -> FileResponse:
    """Encode a message into the source image.

    :param message: Message to encode
    :param file: Source image
    :param delim: ...
    :param lsb_n: ...
    :param rev: ...

    """
    try:
        data = api_encode(message, file, delim, lsb_n, rev)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args) from e

    fp = settings.image_folder / file.filename
    save_image(data, fp)
    try:
        return FileResponse(fp)
    finally:
        fp.unlink()
