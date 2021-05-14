"""Test the encode route."""
from __future__ import annotations

from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING, BinaryIO

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from fastapi.testclient import TestClient


def test_get(api_client: TestClient, api_name: str) -> None:
    """Test the get request of the encode route."""
    response = api_client.get("/encode")
    assert response.status_code == 200
    assert response.json() == {"app-name": api_name}


@pytest.mark.parametrize(
    "message, delimiter, lsb_n",
    [("message", "test/*/", 2), ("secret", "/*/test", 6)],
)
def test_post_success(
    api_client: TestClient,
    api_image_file: dict[str, tuple[str, BinaryIO, str]],
    test_image_path: Path,
    message: str,
    delimiter: str,
    lsb_n: int,
) -> None:
    """Test the post request of the encode route."""
    response = api_client.post(
        f"/encode?message={message}&custom-delimiter={delimiter}&least-significant-bit-amount={lsb_n}",
        files=api_image_file,
    )

    assert response.status_code == 200
    assert isinstance(response.content, bytes)
    with pytest.raises(JSONDecodeError):
        response.json()

    headers = response.headers
    assert headers["filename"] == f"'{test_image_path.name}'"
    assert headers["custom-delimiter"] == f"'{delimiter}'"
    assert headers["least-significant-bit-amount"] == str(lsb_n)
    assert headers["reversed-encoding"] == str(False)
    assert headers["message"] == f"'{message}'"
    assert headers["content-type"] == "image/png"
    assert "test.png" in headers["content-disposition"]


def test_post_msg_too_long(
    api_client: TestClient,
    api_image_file: dict[str, tuple[str, BinaryIO, str]],
) -> None:
    """Test a response with a message longer than allowed."""
    response = api_client.post(
        f"/encode?message={'long-message'*100}",
        files=api_image_file,
    )

    assert response.status_code == 400
    assert "is not enough for the message (1,200)." in response.content.decode()
    assert "long-message" in response.headers["message"]
