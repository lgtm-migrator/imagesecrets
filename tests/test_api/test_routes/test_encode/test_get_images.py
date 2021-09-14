from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

    from imagesecrets.database.image.models import EncodedImage  # noqa
    from imagesecrets.database.image.services import ImageService
    from imagesecrets.database.user.models import User


URL = "api/encode"


def test_get_images(
    api_client: TestClient,
    return_encoded: EncodedImage,
    return_user: User,
    image_service: ImageService,
    access_token,
) -> None:
    """Test a successful get request for decoded images with specified name."""
    image_service.get_encoded.return_value = [return_encoded]

    response = api_client.get(
        f"{URL}/{return_encoded.image_name}",
        headers=access_token,
    )

    image_service.get_encoded.assert_called_once_with(
        user_id=return_user.id,
        image_name=return_encoded.image_name,
    )
    assert response.status_code == 200
    json_ = response.json()
    assert isinstance(json_, list)
    assert len(json_) == 1
    image = json_[0]
    assert image["image_name"] == return_encoded.image_name
    assert image["message"] == return_encoded.message
    assert image["delimiter"] == return_encoded.delimiter
    assert image["lsb_amount"] == return_encoded.lsb_amount


@pytest.mark.parametrize("image_name", ["test_name", "test_url", "10"])
def test_get_images_404(
    api_client: TestClient,
    return_encoded: EncodedImage,
    return_user: User,
    image_service: ImageService,
    access_token,
    image_name: str,
) -> None:
    """Test a successful get request for decoded images without finding any results."""
    image_service.get_encoded.return_value = []

    response = api_client.get(
        f"{URL}/{image_name}",
        headers=access_token,
    )

    image_service.get_encoded.assert_called_once_with(
        user_id=return_user.id,
        image_name=image_name,
    )
    assert response.status_code == 404
    json_ = response.json()
    assert (
        json_["detail"]
        == f"no encoded image(s) with name {image_name!r} found"
    )
