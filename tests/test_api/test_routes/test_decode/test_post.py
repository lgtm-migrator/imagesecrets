from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from pytest import MockFixture

    from imagesecrets.database.image.models import DecodedImage  # noqa
    from imagesecrets.database.image.services import ImageService
    from imagesecrets.database.user.models import User

URL = "api/decode"


@pytest.mark.parametrize(
    "delimiter, lsb_n",
    [
        ("dlm1", 1),
        ("dlm2", 2),
        ("dlm3", 3),
        ("dlm5", 4),
        ("dlm5", 5),
        ("dlm6", 6),
        ("dlm7", 7),
        ("dlm8", 8),
    ],
)
def test_post(
    api_client: TestClient,
    image_service: ImageService,
    return_user: User,
    access_token,
    api_image_file,
    test_image_path: Path,
    mocker: MockFixture,
    delimiter: str,
    lsb_n: int,
) -> None:
    """Test a successful post request."""
    from imagesecrets.database.image.models import DecodedImage  # noqa

    new_decoded = DecodedImage(
        image_name="test_image_name",
        message="test_message",
        delimiter=delimiter,
        lsb_amount=lsb_n,
        filename="test_filename",
        created=datetime(year=2000, month=1, day=1),
        updated=datetime(year=3000, month=2, day=2),
        user_id=return_user.id,
    )

    image_service.create_decoded.return_value = new_decoded

    buffer = api_image_file["file"][1]

    decode_api = mocker.patch(
        "imagesecrets.core.decode.api",
        return_value=("decoded>test", test_image_path),
    )

    response = api_client.post(
        URL,
        files=api_image_file,
        data={
            "custom-delimiter": delimiter,
            "least-significant-bit-amount": lsb_n,
        },
        headers=access_token,
    )

    decode_api.assert_called_once_with(
        image_data=buffer,
        delimiter=delimiter,
        lsb_n=lsb_n,
        reverse=False,
    )

    assert response.status_code == 201
    json_ = response.json()
    assert json_["image_name"] == new_decoded.image_name
    assert json_["message"] == new_decoded.message
    assert json_["delimiter"] == delimiter
    assert json_["lsb_amount"] == lsb_n


def test_post_200(
    api_client: TestClient,
    access_token,
    mocker: MockFixture,
    test_image_path: Path,
    api_image_file,
) -> None:
    """Test a post request with valid request but no decoded result."""
    buffer = api_image_file["file"][1]

    decode_api = mocker.patch(
        "imagesecrets.core.decode.api",
    )
    decode_api.side_effect = StopIteration("test exception")

    response = api_client.post(
        URL,
        files=api_image_file,
        data={
            "custom-delimiter": "delimiter",
            "least-significant-bit-amount": 1,
        },
        headers=access_token,
    )

    decode_api.assert_called_once_with(
        image_data=buffer,
        delimiter="delimiter",
        lsb_n=1,
        reverse=False,
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "test exception"
    headers = response.headers
    assert headers["custom-delimiter"] == "delimiter"
    assert headers["least-significant-bit-amount"] == repr(1)


def test_post_415(
    api_client: TestClient,
    access_token,
) -> None:
    """Test a post request with invalid media type."""
    response = api_client.post(
        URL,
        files={
            "file": (Path(__file__).name, open(__file__).read(), "image/png"),
        },
        headers=access_token,
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "only .png images are supported"
