from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


URL = "/users/me"


def test_delete(
    api_client: TestClient,
    access_token,
) -> None:
    """Test a successful delete request."""
    response = api_client.delete(
        URL,
        headers=access_token,
    )

    assert response.status_code == 202
    assert response.reason == "Accepted"
    assert response.json()["detail"] == "account deleted"
