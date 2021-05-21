"""CRUD operation with images via databse."""

from image_secrets.backend.database.image import models, schemas


async def create_decoded(
    owner_id: int,
    data: schemas.ImageCreate,
) -> models.DecodedImage:
    image = await models.DecodedImage.create(owner_id=owner_id, **data.dict())
    return image


async def create_encoded(
    owner_id: int,
    data: schemas.ImageCreate,
) -> models.EncodedImage:
    image = await models.EncodedImage.create(owner_id=owner_id, **data.dict())
    return image
