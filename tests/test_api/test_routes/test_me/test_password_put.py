from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from pytest_mock import MockFixture

    from imagesecrets.database.user.services import UserService

URL = "api/users/me"


def test_password_put(
    api_client: TestClient,
    user_service: UserService,
    return_user,
    access_token,
) -> None:
    """Test a successful password put request."""
    user_service.authenticate.return_value = True

    old_password = "old_password"
    new_password = "new_password"

    response = api_client.put(
        f"{URL}/password",
        headers=access_token,
        data={"old": old_password, "new": new_password},
    )

    user_service.authenticate.assert_called_once_with(
        username=return_user.username,
        password_=old_password,
    )
    assert response.status_code == 202
    assert response.reason == "Accepted"
    assert response.json()["detail"] == "account password updated"


def test_password_put_401(
    mocker: MockFixture,
    api_client: TestClient,
    user_service: UserService,
    return_user,
    access_token,
) -> None:
    """Test a password put request with invalid password in request body"""
    user_service.authenticate.return_value = False

    old_password = "old_password"
    new_password = "new_password"

    response = api_client.put(
        f"{URL}/password",
        headers=access_token,
        data={"old": old_password, "new": new_password},
    )

    user_service.authenticate.assert_called_once_with(
        username=return_user.username,
        password_=old_password,
    )
    assert response.status_code == 401
    assert response.reason == "Unauthorized"
    assert response.json() == {"detail": "incorrect password"}
