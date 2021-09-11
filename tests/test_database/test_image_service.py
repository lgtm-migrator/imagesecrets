import pytest
from pytest_mock import MockFixture

from imagesecrets.database.image.models import DecodedImage, EncodedImage
from imagesecrets.schemas import ImageCreate


@pytest.mark.asyncio
async def test_service_get(mocker, image_service):
    return_value = mocker.Mock()
    return_value.scalars = mocker.Mock(return_value=[1, 2, 3])
    image_service._session.execute.return_value = return_value

    result = await image_service._get(
        model=DecodedImage,
        user_id=0,
        image_name="test image name",
    )

    return_value.scalars.assert_called_once_with()
    assert result == [1, 2, 3]


@pytest.mark.asyncio
async def test_service_get_decoded(mocker: MockFixture, image_service):
    service_get = mocker.patch(
        "imagesecrets.database.image.services.ImageService._get",
        return_value="get called",
    )

    result = await image_service.get_decoded(user_id=0)

    service_get.assert_called_once_with(
        model=DecodedImage,
        user_id=0,
        image_name=None,
    )

    assert result == "get called"


@pytest.mark.asyncio
async def test_service_get_encoded(mocker: MockFixture, image_service):
    service_get = mocker.patch(
        "imagesecrets.database.image.services.ImageService._get",
        return_value="get called",
    )

    result = await image_service.get_encoded(user_id=0)

    service_get.assert_called_once_with(
        model=EncodedImage,
        user_id=0,
        image_name=None,
    )

    assert result == "get called"


@pytest.mark.asyncio
async def test_service_create_decoded(image_service):
    result = await image_service.create_decoded(
        user_id=0,
        data=ImageCreate(
            filename="test filename",
            image_name="test image name",
            message="test message",
        ),
    )

    image_service._session.add.assert_called_once_with(result)
    assert isinstance(result, DecodedImage)


@pytest.mark.asyncio
async def test_service_create_encoded(image_service):
    result = await image_service.create_encoded(
        user_id=0,
        data=ImageCreate(
            filename="test filename",
            image_name="test image name",
            message="test message",
        ),
    )

    image_service._session.add.assert_called_once_with(result)
    assert isinstance(result, EncodedImage)
