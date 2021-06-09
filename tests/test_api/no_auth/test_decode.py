"""Test the decode router without user authentication."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from requests import HTTPError

if TYPE_CHECKING:
    from pathlib import Path

    from fastapi.testclient import TestClient


URL = "/decode"


def test_get(api_client: TestClient) -> None:
    """Test the get request of the encode route without using an access token."""
    response = api_client.get(URL)
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


@pytest.mark.parametrize(
    "delimiter, lsb_n",
    [("test/*/", 2), ("/*/test", 6)],
)
def test_post(
    api_client: TestClient,
    api_image_file: dict[str, Any],
    test_image_path: Path,
    delimiter: str,
    lsb_n: int,
) -> None:
    """Test the post request of the encode route."""
    response = api_client.post(
        URL,
        files=api_image_file
        | {
            "custom-delimiter": delimiter,
            "least-significant-bit-amount": lsb_n,
        },
    )

    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


@pytest.mark.parametrize(
    "image_name",
    ["0", "test_image_name"],
)
def test_get_images(
    api_client: TestClient,
    api_image_file: dict[str, Any],
    test_image_path: Path,
    image_name: str,
) -> None:
    """Test the get request for specified decoded images."""
    response = api_client.get(f"{URL}/{image_name}")

    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"
