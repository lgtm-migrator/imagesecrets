"""Test the encode router without user authentication."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from requests.exceptions import HTTPError

if TYPE_CHECKING:
    from pathlib import Path

    from fastapi.testclient import TestClient


def test_get(api_client: TestClient) -> None:
    """Test the get request of the encode route without using an access token."""
    response = api_client.get("/encode")
    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"


@pytest.mark.parametrize(
    "message, delimiter, lsb_n",
    [("message", "test/*/", 2), ("secret", "/*/test", 6)],
)
def test_post(
    api_client: TestClient,
    api_image_file: dict[str, Any],
    test_image_path: Path,
    message: str,
    delimiter: str,
    lsb_n: int,
) -> None:
    """Test the post request of the encode route."""
    response = api_client.post(
        "/encode",
        files=api_image_file
        | {
            "message": message,
            "custom-delimiter": delimiter,
            "least-significant-bit-amount": lsb_n,
        },
    )

    with pytest.raises(HTTPError):
        response.raise_for_status()
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "invalid access token"
