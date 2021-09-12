from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from imagesecrets.database.user.models import User


@pytest.fixture()
def access_token() -> dict[str, str]:
    return {"authorization": f'{"token_type".capitalize()} {"access_token"}'}


@pytest.fixture()
def return_user() -> User:
    """Return a fake database user entry."""
    from imagesecrets.database.user.models import User

    return User(
        id=1,
        username="test_username",
        email="test@email.com",
        password_hash="test_hash",
        created=datetime(year=2000, month=1, day=1),
        updated=datetime(year=3000, month=2, day=2),
    )
