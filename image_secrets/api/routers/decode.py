"""Decode router."""
from fastapi import APIRouter, Depends, File, Query, UploadFile

from image_secrets.api import config
from image_secrets.api.dependencies import get_settings
from image_secrets.api.schemas import DecodeSchema
from image_secrets.backend import decode as b_decode
from image_secrets.settings import MESSAGE_DELIMITER

router = APIRouter(
    tags=["decode"],
    dependencies=[Depends(get_settings)],
)


@router.get("/decode/")
async def decode_home(settings: config.Settings = Depends(get_settings)) -> dict:
    return {"app-name": settings.app_name}


@router.post("/decode")
async def decode(
    *,
    file: UploadFile = File(
        ...,
        description="The image from which to decode the message.",
    ),
    delim: str = Query(
        MESSAGE_DELIMITER,
        description="""The previously defined message delimiter.""",
        alias="custom-delimiter",
    ),
    lsb_n: int = Query(
        1,
        title="Number of least significant bits which have beed used to encode the message.",
        ge=1,
        le=8,
        alias="least-significant-bit-amount",
    ),
    rev: bool = Query(
        False,
        alias="reversed-encoding",
        description="Whether the message was encoded in reverse.",
    ),
) -> DecodeSchema:
    """Decode a message from an image.

    - **file**: The image
    - **custom-delimiter**: String which identifies the end of the encoded message.
    - **least-significant-bit-amount**: Number of least significant bits which was used to encode the message.
    - **reversed-encoding**: Whether the message was encoded in reverse.

    \f
    :param file: Source image
    :param delim: Message delimiter, defaults to 'MESSAGE_DELIMITER'
    :param lsb_n: Number of lsb to use, defaults to 1
    :param rev: Reverse encoding bool, defaults to False

    """
    data = await file.read()
    try:
        decoded = b_decode.api(data, delim, lsb_n, rev)
    except StopIteration:
        decoded = None
    return DecodeSchema(
        message=decoded,
        filename=file.filename,
        delimiter=delim,
        least_significant_bits=lsb_n,
        reverse_decoding=rev,
    )


__all__ = ["decode", "decode_home", "router"]
