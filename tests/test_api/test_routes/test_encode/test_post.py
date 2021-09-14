from __future__ import annotations

from json import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from pytest import MockFixture

    from imagesecrets.database.image.models import DecodedImage  # noqa

URL = "/encode"


@pytest.mark.parametrize(
    "message, delimiter, lsb_n",
    [
        ("test1", "dlm1", 1),
        ("test2", "dlm2", 2),
        ("test3", "dlm3", 3),
        ("test4", "dlm5", 4),
        ("test5", "dlm5", 5),
        ("test6", "dlm6", 6),
        ("test7", "dlm7", 7),
        ("test8", "dlm8", 8),
    ],
)
def test_post(
    api_client: TestClient,
    api_image_file,
    test_image_path: Path,
    mocker: MockFixture,
    message: str,
    delimiter: str,
    lsb_n: int,
    access_token,
) -> None:
    """Test a successful post request."""
    buffer = api_image_file["file"][1]

    encode_api = mocker.patch(
        "imagesecrets.core.encode.api",
        return_value=test_image_path,
    )

    response = api_client.post(
        URL,
        files=api_image_file,
        data={
            "message": message,
            "custom-delimiter": delimiter,
            "least-significant-bit-amount": lsb_n,
        },
        headers=access_token,
    )

    encode_api.assert_called_once_with(
        message=message,
        file=buffer,
        delimiter=delimiter,
        lsb_n=lsb_n,
        reverse=False,
    )

    assert response.status_code == 201
    with pytest.raises(JSONDecodeError):  # png image data should be returned
        response.json()
    headers = response.headers
    assert headers["image-name"] == "test.png"
    assert headers["message"] == message
    assert headers["delimiter"] == delimiter
    assert headers["lsb_amount"] == repr(lsb_n)
    assert headers["content-type"] == "image/png"
    assert 'filename="test.png"' in headers["content-disposition"]


def test_post_image_too_small(
    api_client: TestClient,
    api_image_file,
    access_token,
) -> None:
    """Test a post request with a message longer than fits into the uploaded image."""
    msg = "test" * 1000
    response = api_client.post(
        URL,
        files=api_image_file,
        data={"message": msg},
        headers=access_token,
    )

    assert response.status_code == 422
    json_ = response.json()
    assert json_["field"] == "file"
    headers = response.headers
    assert headers["image-name"] == "test.png"
    assert headers["message"] == msg
    assert headers["delimiter"] == "<{~stop-here~}>"
    assert headers["lsb_amount"] == repr(1)


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
        data={"message": "test message"},
        headers=access_token,
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "only .png images are supported"
