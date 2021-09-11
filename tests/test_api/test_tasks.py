"""Test API tasks module."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

from imagesecrets.api import tasks

if TYPE_CHECKING:
    from unittest.mock import AsyncMock

    from pytest_mock import MockFixture


@pytest.fixture()
def mock_sleep(mocker: MockFixture):
    """Return mocked ``asyncio.sleep``."""
    async_mock = mocker.AsyncMock(return_value=None)
    return mocker.patch(
        "asyncio.sleep",
        side_effect=async_mock,
    )


def test_repeat(mock_sleep: AsyncMock) -> None:
    """Test a successful repeat function call."""

    @tasks.repeat(seconds=1)
    async def test_coro() -> None:
        """Testing coroutine."""
        raise RuntimeError

    asyncio.run(test_coro())

    mock_sleep.assert_called_once_with(1)
