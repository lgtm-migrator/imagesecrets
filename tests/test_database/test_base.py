import pytest
from pytest_mock import MockFixture


@pytest.mark.asyncio
async def test_get_session(mocker: MockFixture, async_context_manager):
    from imagesecrets.database import base

    begin = mocker.patch(
        "imagesecrets.database.base.async_sessionmaker.begin",
        return_value=async_context_manager,
    )

    async with base.get_session() as result:
        ...

    begin.assert_called_once_with()
    assert result is None


@pytest.mark.asyncio
async def test_startup(mocker: MockFixture, async_context_manager):
    from imagesecrets.database import base
    from imagesecrets.interface import app

    engine = mocker.Mock()

    conn = mocker.Mock()
    conn.run_sync = mocker.AsyncMock()

    async_context_manager.obj = conn

    engine.begin = mocker.Mock(return_value=async_context_manager)

    mocker.patch(
        "imagesecrets.database.base.engine",
        return_value=engine,
    )

    base.init(app=app)

    for func in app.router.on_startup:
        # need to find correct function
        # for now we just need to find the only task from `api.tasks`
        if func.__module__ != "imagesecrets.database.base":
            continue

        await func()
