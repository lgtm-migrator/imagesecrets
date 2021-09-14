from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy.exc import NoResultFound

from imagesecrets.api.exceptions import NotAuthenticated

if TYPE_CHECKING:
    from imagesecrets.database.user.services import UserService


def test_get_config():
    from imagesecrets.api import dependencies
    from imagesecrets.config import settings

    config = dependencies.get_config()

    assert config is settings


@pytest.mark.asyncio
async def test_user_loader_ok(
    api_client,
    user_service: UserService,
):
    from imagesecrets.api.routers.user.main import manager

    user_service.get.return_value = "test_user"

    result = await manager._user_callback("test_identifier")

    assert result == "test_user"


@pytest.mark.asyncio
async def test_user_loader_no_result(
    api_client,
    user_service: UserService,
):
    from imagesecrets.api.routers.user.main import manager

    user_service.get.side_effect = NoResultFound

    with pytest.raises(NotAuthenticated):
        await manager._user_callback("test_identifier")
