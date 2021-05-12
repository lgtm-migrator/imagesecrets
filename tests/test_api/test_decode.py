"""Test the decode route."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from fastapi.testclient import TestClient


def test_get(api_client: TestClient, api_name) -> None:
    """Test the get request of the decode route."""
    response = api_client.get("/decode")
    assert response.status_code == 200
    assert response.json() == {"app-name": api_name}


def test_post(api_client: TestClient, api_name: str, test_image_path: Path) -> None:
    """Test the post request of the encode route."""
    response = api_client.post(
        "/decode",
        files={"file": ("test.png", test_image_path.open("rb"), "image/png")},
    )
    assert response.status_code == 400
    assert (
        "No message found after scanning the whole image." in response.content.decode()
    )

    assert response.headers["filename"] == "'test.png'"
    assert response.headers["delimiter"] == "'<{~stop-here~}>'"
    assert response.headers["least-significant-bits"] == "1"
    assert response.headers["reverse-decoding"] == "False"
    assert response.headers["content-length"] == "63"
    assert response.headers["content-type"] == "application/json"
