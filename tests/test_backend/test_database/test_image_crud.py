"""Test the CRUD module for images."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets.backend.database.image import crud

if TYPE_CHECKING:
    from pytest_mock import MockFixture

    from image_secrets.backend.database.image.models import DecodedImage, EncodedImage
    from image_secrets.backend.database.image.schemas import ImageCreate


@pytest.fixture()
def image_create() -> ImageCreate:
    """Return an ``ImageCreate`` schema."""
    from image_secrets.backend.database.image import schemas

    create = schemas.ImageCreate(
        message="test_message",
        image_name="test_name",
        filename="test_filename.png",
    )
    return create


@pytest.fixture()
def decoded_image() -> DecodedImage:
    """Return a decoded image."""
    from image_secrets.backend.database.image import models

    image = models.DecodedImage(
        filename="test_filename.png",
        image_name="test_image_name",
        message="test_message",
        delimiter="test_delimiter",
        lsb_amount=2,
    )
    return image


@pytest.fixture()
def encoded_image() -> EncodedImage:
    """Return an encoded image."""
    from image_secrets.backend.database.image import models

    image = models.EncodedImage(
        filename="test_filename.png",
        image_name="test_image_name",
        message="test_message",
        delimiter="test_delimiter",
        lsb_amount=2,
    )
    return image


@pytest.fixture()
def mock_create_decoded(mocker: MockFixture, decoded_image: DecodedImage):
    """Return mocked DecodedImage.create function."""
    async_mock = mocker.AsyncMock(return_value=decoded_image)
    return mocker.patch(
        "image_secrets.backend.database.image.models.DecodedImage.create",
        side_effect=async_mock,
    )


@pytest.fixture()
def mock_create_encoded(mocker: MockFixture, encoded_image: EncodedImage):
    """Return mocked EncodedImage.create function."""
    async_mock = mocker.AsyncMock(return_value=encoded_image)
    return mocker.patch(
        "image_secrets.backend.database.image.models.EncodedImage.create",
        side_effect=async_mock,
    )


@pytest.mark.asyncio
async def test_create_decoded(
    mock_create_decoded,
    decoded_image: DecodedImage,
    image_create: ImageCreate,
) -> None:
    """Test the create_decoded function."""
    from image_secrets.backend.database.image import models

    result = await crud.create_decoded(0, image_create)

    assert isinstance(result, models.DecodedImage)
    assert result == decoded_image
    mock_create_decoded.assert_called_once_with(owner_id=0, **image_create.dict())


@pytest.mark.asyncio
async def test_create_encoded(
    mock_create_encoded,
    encoded_image: EncodedImage,
    image_create: ImageCreate,
) -> None:
    """Test the create_encoded function."""
    from image_secrets.backend.database.image import models

    result = await crud.create_encoded(0, image_create)

    assert isinstance(result, models.EncodedImage)
    assert result == encoded_image
    mock_create_encoded.assert_called_once_with(owner_id=0, **image_create.dict())
