from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from starlette.responses import JSONResponse

from imagesecrets.api import handlers

if TYPE_CHECKING:
    from pytest_mock import MockFixture


def test_init(mocker: MockFixture) -> None:
    app = mocker.Mock()

    handler = mocker.Mock()
    app.exception_handler = mocker.Mock(return_value=handler)

    handlers.init(app=app)

    assert app.exception_handler.call_count == 3
    assert handler.call_count == 3


@pytest.mark.asyncio
async def test_handler_no_value() -> None:
    result = await handlers.handler(
        status_code=200,
        message="test_message",
        field="test_field",
    )

    assert isinstance(result, JSONResponse)
    assert result.status_code == 200
    assert result.body == b'{"detail":"test_message","field":"test_field"}'


@pytest.mark.asyncio
async def test_handler_with_value() -> None:
    result = await handlers.handler(
        status_code=200,
        message="test_message",
        field="test_field",
        value="test_value",
    )

    assert isinstance(result, JSONResponse)
    assert result.status_code == 200
    assert (
        result.body
        == b'{"detail":"test_message","field":"test_field","value":"test_value"}'
    )


@pytest.mark.asyncio
async def test_not_authenticated(mocker: MockFixture) -> None:
    exc = mocker.Mock()
    exc.status_code = 200

    result = await handlers.not_authenticated(req=..., exc=exc)

    assert isinstance(result, JSONResponse)
    assert result.status_code == 200
    assert result.body == b'{"detail":"invalid access token"}'
