"""Test the decode route."""
from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO

import pytest

from image_secrets.settings import MESSAGE_DELIMITER

if TYPE_CHECKING:
    from pathlib import Path

    from fastapi.testclient import TestClient


def test_get(api_client: TestClient, api_name) -> None:
    """Test the get request of the decode route."""
    response = api_client.get("/decode")
    assert response.status_code == 200
    assert response.json() == {"app-name": api_name}


@pytest.mark.parametrize(
    "delimiter, lsb_n, rev",
    [
        ("ABC", 3, True),
        (MESSAGE_DELIMITER, 5, True),
        ("123456789", 7, False),
    ],
)
def test_post_fail(
    api_client: TestClient,
    api_image_file: dict[str, tuple[str, BinaryIO, str]],
    test_image_path: Path,
    delimiter: str,
    lsb_n: int,
    rev: bool,
) -> None:
    """Test the post request of the encode route with an image which has nothing encoded."""
    response = api_client.post(
        f"/decode?custom-delimiter={delimiter}&least-significant-bit-amount={lsb_n}&reversed-encoding={rev}",
        files=api_image_file,
    )

    assert response.status_code == 400
    assert (
        "No message found after scanning the whole image." in response.json()["detail"]
    )

    headers = response.headers
    assert headers["filename"] == f"'{test_image_path.name}'"
    assert headers["custom-delimiter"] == f"'{delimiter}'"
    assert headers["least-significant-bit-amount"] == str(lsb_n)
    assert headers["reversed-encoding"] == str(rev)
    assert headers["content-length"] == str(63)
    assert headers["content-type"] == "application/json"


@pytest.mark.parametrize("lsb_n,", [-1, 0, 9, 100])
def test_post_invalid_lsb(
    api_client: TestClient,
    api_image_file: dict[str, tuple[str, BinaryIO, str]],
    lsb_n: int,
) -> None:
    """Test the post request of the encode route with invalid arguments."""
    response = api_client.post(
        f"/decode?least-significant-bit-amount={lsb_n}",
        files=api_image_file,
    )

    json_ = response.json()
    assert response.status_code == 422
    assert json_["detail"][0]["loc"][-1] == "least-significant-bit-amount"
    assert (
        f"value_error.number.not_{'ge' if lsb_n < 1 else 'le'}"
        in response.content.decode()
    )
    assert response.headers["content-type"] == "application/json"
