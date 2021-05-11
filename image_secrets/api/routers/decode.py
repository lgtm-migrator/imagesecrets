"""Decode router."""
from typing import Union

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from image_secrets.api import config
from image_secrets.api.dependencies import get_settings
from image_secrets.api.schemas import DecodeSchema
from image_secrets.backend import decode as b_decode
from image_secrets.settings import MESSAGE_DELIMITER

router = APIRouter(
    tags=["decode"],
    dependencies=[Depends(get_settings)],
)


@router.get("/decode/", response_model=dict, summary="Information about decode route")
async def decode_home(settings: config.Settings = Depends(get_settings)) -> dict:
    return {"app-name": settings.app_name}


@router.post(
    "/decode",
    response_model=dict[str, Union[str, DecodeSchema]],
    summary="Decode a message from an image",
    responses={
        200: {
            "model": dict[str, Union[str, DecodeSchema]],
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Secret message!",
                        "decode-arguments": {
                            "custom-delimiter": MESSAGE_DELIMITER,
                            "least-significant-bit-amount": 1,
                            "reversed-encoding": False,
                        },
                    },
                },
            },
        },
        400: {
            "description": "Decoding Failure",
            "content": {
                "application/json": {
                    "example": {
                        "detail": ["Something went wrong while decoding."],
                    },
                },
            },
        },
    },
)
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
) -> dict[str, Union[str, DecodeSchema]]:
    """Decode a message from an image.

    - **file**: The image
    - **custom-delimiter**: String which identifies the end of the encoded message.
    - **least-significant-bit-amount**: Number of least significant bits which was used to encode the message.
    - **reversed-decoding**: Whether the message was encoded in reverse.

    \f
    :param file: Source image
    :param delim: Message delimiter, defaults to 'MESSAGE_DELIMITER'
    :param lsb_n: Number of lsb to use, defaults to 1
    :param rev: Reverse encoding bool, defaults to False

    """
    schema = DecodeSchema(
        filename=file.filename,
        delimiter=delim,
        least_significant_bits=lsb_n,
        reverse_decoding=rev,
    )

    data = await file.read()
    try:
        decoded = b_decode.api(data, delim, lsb_n, rev)
    except StopIteration as e:
        raise HTTPException(
            status_code=400,
            detail=e.args,
            headers={
                key.replace("_", "-"): repr(value)
                for key, value in schema  # bool and int are not hashable
            },
        ) from e
    return {"message": decoded, "decode-arguments": schema}


__all__ = ["decode", "decode_home", "router"]
