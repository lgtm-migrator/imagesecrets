import contextlib

import pytest
from pytest_mock import MockFixture

from imagesecrets.database.service import DatabaseService


@pytest.mark.asyncio
async def test_service_from_session(
    mocker: MockFixture,
    async_context_manager,
):
    get_session = mocker.patch(
        "imagesecrets.database.base.get_session",
        return_value=async_context_manager,
    )

    async with contextlib.asynccontextmanager(
        DatabaseService.from_session,
    )() as result:
        ...

    get_session.assert_called_once_with()
    assert isinstance(result, DatabaseService)
    assert result._session is None
