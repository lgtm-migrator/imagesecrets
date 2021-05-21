"""CRUD operation with images via database."""

from image_secrets.backend.database.image import models, schemas


async def create_decoded(
    owner_id: int,
    data: schemas.ImageCreate,
) -> models.DecodedImage:
    """Insert a new encoded image.

    :param owner_id: User foreign key
    :param data: Image information

    """
    image = await models.DecodedImage.create(owner_id=owner_id, **data.dict())
    return image


async def create_encoded(
    owner_id: int,
    data: schemas.ImageCreate,
) -> models.EncodedImage:
    """Insert a new decoded image.

    :param owner_id: User foreign key
    :param data: Image information

    """
    image = await models.EncodedImage.create(owner_id=owner_id, **data.dict())
    return image
