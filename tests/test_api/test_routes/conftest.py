from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from imagesecrets.database.user.models import User


@pytest.fixture(autouse=True)
def patch_manager_call(monkeypatch, return_user):
    monkeypatch.setattr(
        "fastapi_login.LoginManager.__call__",
        lambda *a, **kw: return_user,
    )


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


@pytest.fixture()
def return_decoded(return_user) -> User:
    """Return a fake database decodedimage entry."""
    from imagesecrets.database.image.models import DecodedImage

    return DecodedImage(
        image_name="test_image_name",
        message="test_message",
        delimiter="test_delimiter",
        lsb_amount=1,
        filename="test_filename",
        created=datetime(year=2000, month=1, day=1),
        updated=datetime(year=3000, month=2, day=2),
        user_id=return_user.id,
    )


@pytest.fixture()
def return_encoded(return_user) -> User:
    """Return a fake database encodedimage entry."""
    from imagesecrets.database.image.models import EncodedImage

    return EncodedImage(
        image_name="test_image_name",
        message="test_message",
        delimiter="test_delimiter",
        lsb_amount=1,
        filename="test_filename",
        created=datetime(year=2000, month=1, day=1),
        updated=datetime(year=3000, month=2, day=2),
        user_id=return_user.id,
    )
