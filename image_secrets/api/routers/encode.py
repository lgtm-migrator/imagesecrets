"""Router for the encoding operations."""
from typing import Optional, Union

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from filetype import filetype

from image_secrets.api import dependencies, exceptions, responses
from image_secrets.api.routers.users.main import manager
from image_secrets.backend import encode
from image_secrets.backend.database.image import crud
from image_secrets.backend.database.image import schemas as image_schemas
from image_secrets.backend.database.user import models
from image_secrets.settings import MESSAGE_DELIMITER

router = APIRouter(
    tags=["encode"],
    dependencies=[Depends(dependencies.get_config)],
)


@router.get(
    "/encode",
    response_model=list[Optional[image_schemas.Image]],
    status_code=status.HTTP_200_OK,
    summary="Encoded images",
    responses=responses.AUTHORIZATION | responses.FORBIDDEN | responses.IMAGE_TOO_SMALL,
)
async def get(
    current_user: models.User = Depends(manager),
) -> list[Optional[image_schemas.Image]]:
    """Return all encoded images.

    \f
    :param current_user: Current user dependency

    """
    await current_user.fetch_related("encoded_images")
    # not using from_tortoise_orm because it would try to prefetch the owner FK relation
    images = [
        image_schemas.Image.from_orm(image)
        async for image in current_user.encoded_images
    ]
    return images


@router.post(
    "/encode",
    status_code=status.HTTP_201_CREATED,
    response_class=FileResponse,
    summary="Encode a message into an image",
    responses=responses.AUTHORIZATION | responses.FORBIDDEN | responses.MEDIA,
)
async def encode_message(
    current_user: models.User = Depends(manager),
    message: str = Form(
        ...,
        title="Message to encode",
        description="The message to encode into the image.",
        min_length=1,
        example="My secret message!",
    ),
    file: UploadFile = File(
        ...,
        media_type="image/png",
        description="The image in which to encode the message.",
    ),
    delim: str = Form(
        MESSAGE_DELIMITER,
        alias="custom-delimiter",
        description="""String which is going to be appended to the end of your message
        so that the message can be decoded later.""",
        min_length=1,
    ),
    lsb_n: int = Form(
        1,
        alias="least-significant-bit-amount",
        description="Number of least significant bits to alter.",
        ge=1,
        le=8,
    ),
) -> Union[FileResponse, JSONResponse]:
    """Encode a message into an image.

    - **message**: The message to encode into the image
    - **file**: The image
    - **custom-delimiter**: String which is going to be appended to the end of your message
        so that the message can be decoded later.
    - **least-significant-bit-amount**: Number of least significant bits to alter.

    \f
    :param current_user: Current user dependency
    :param message: Message to encode
    :param file: Source image
    :param delim: Message delimiter, defaults to 'MESSAGE_DELIMITER'
    :param lsb_n: Number of lsb to use, defaults to 1

    """
    headers = {
        "image-name": file.filename,
        "message": message,
        "delimiter": delim,
        "lsb_amount": repr(lsb_n),
    }
    data = await file.read()

    if not filetype.match(data).extension == "png":
        raise exceptions.UnsupportedMediaType(headers=headers)

    try:
        fp = encode.api(message, data, delim, lsb_n, False)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": e.args[0], "field": "file"},
        )
    image_schema = image_schemas.ImageCreate(
        delimiter=delim,
        lsb_amount=lsb_n,
        message=message,
        image_name=file.filename,
        filename=fp.name,
    )
    await crud.create_encoded(owner_id=current_user.id, data=image_schema)
    return FileResponse(
        fp,
        media_type="image/png",
        filename=image_schema.filename,
        headers=headers,
    )


__all__ = [
    "encode_message",
    "router",
]
