"""Image database models."""
from tortoise import fields
from tortoise.models import Model

from image_secrets.backend.database.image.fields import LSBIntField
from image_secrets.settings import MESSAGE_DELIMITER


class Image(Model):
    """Tortoise base image model."""

    id = fields.IntField(pk=True, index=True)

    filename = fields.CharField(max_length=128, unique=True, index=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    image_name = fields.CharField(max_length=128)
    message = fields.TextField()
    delimiter = fields.TextField(default=MESSAGE_DELIMITER)
    lsb_amount = LSBIntField(default=1)

    class Meta:
        """Tortoise metaclass setup."""

        abstract = True


class DecodedImage(Image):
    """Tortoise decoded image model."""

    owner = fields.ForeignKeyField(
        "models.User",
        related_name="decoded_images",
        on_delete=fields.CASCADE,
    )

    class Meta:
        """Tortoise metaclass."""

        table = "decode_image"


class EncodedImage(Image):
    """Tortoise encoded image model."""

    owner = fields.ForeignKeyField(
        "models.User",
        related_name="encoded_images",
        on_delete=fields.CASCADE,
    )

    class Meta:
        """Tortoise metaclass."""

        table = "encode_image"


__models__ = [DecodedImage, EncodedImage]

__all__ = [
    "Image",
    "DecodedImage",
    "EncodedImage",
]
