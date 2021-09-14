from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

    from imagesecrets.database.image.models import DecodedImage
    from imagesecrets.database.image.services import ImageService
    from imagesecrets.database.user.models import User

URL = "api/decode"


def test_get_empty(
    api_client: TestClient,
    image_service: ImageService,
    return_user: User,
    access_token,
) -> None:
    """Test the get request with no stored images."""
    image_service.get_decoded.return_value = []

    response = api_client.get(
        URL,
        headers=access_token,
    )

    image_service.get_decoded.assert_called_once_with(user_id=return_user.id)
    assert response.status_code == 200
    json_ = response.json()
    assert isinstance(json_, list)
    assert not json_


def test_get(
    api_client: TestClient,
    image_service: ImageService,
    return_decoded: DecodedImage,
    access_token,
) -> None:
    """Test the get request."""
    image_service.get_decoded.return_value = [return_decoded]

    response = api_client.get(
        URL,
        headers=access_token,
    )

    assert response.status_code == 200
    json_ = response.json()
    assert isinstance(json_, list)
    image = json_[0]
    assert image["image_name"] == return_decoded.image_name
    assert image["message"] == return_decoded.message
    assert image["delimiter"] == return_decoded.delimiter
    assert image["lsb_amount"] == return_decoded.lsb_amount
