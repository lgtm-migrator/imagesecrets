"""Test the forgot password post request."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from pytest_mock import MockFixture

    from image_secrets.backend.database.user.models import User

URL = "/users/forgot-password"


def test_ok(api_client: TestClient, mocker: MockFixture, insert_user: User) -> None:
    """Test a successful request."""
    bg_tasks = mocker.patch("fastapi.BackgroundTasks.add_task", return_value=None)

    response = api_client.post(URL, data={"email": insert_user.email})

    bg_tasks.assert_called_once()
    response.raise_for_status()
    assert response.status_code == 202
    assert response.json() == {
        "detail": "email with the password reset token has been sent",
    }
