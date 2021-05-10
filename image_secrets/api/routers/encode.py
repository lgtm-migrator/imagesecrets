"""Router for the encoding endpoint."""
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
)
from fastapi.responses import FileResponse

from image_secrets.api import config
from image_secrets.api.dependencies import get_settings
from image_secrets.backend import encode
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
async def encode_home(
    settings: config.Settings = Depends(get_settings),
) -> dict[str, str]:
    return {"app-name": settings.app_name}


@router.post("/encode/", summary="Encode a message into an image")
async def encode_message(
    background_tasks: BackgroundTasks,
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
        le=2,
        alias="least-significant-bit-amount",
    ),
    rev: bool = Query(
        False,
        alias="reversed-encoding",
        description="Message will be encoded starting from the last pixel instead of the first one.",
    ),
) -> FileResponse:
    """Encode a message into an image.

    - **message**: The message to encode into the image
    - **file**: The image
    - **custom-delimeter**: String which is going to be appended to the end of your message
        so that the message can be decoded later.
    - **least-significant-bit-amount**: Number of least significant bits to alter.
    - **reversed-encoding**: Message will be encoded starting from the last pixel instead of the first one.

    \f
    :param message: Message to encode
    :param file: Source image
    :param delim: Message delimeter, defaults to 'MESSAGE_DELIMETER'
    :param lsb_n: Number of lsb to use, defaults to 1
    :param rev: Reverse encoding bool, defaults to False

    """
    data = await file.read()
    try:
        fp = encode.api(message, data, delim, lsb_n, rev)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args) from e

    background_tasks.add_task(fp.unlink)
    return FileResponse(fp)


__all__ = [
    "encode_home",
    "encode_message",
    "router",
]
