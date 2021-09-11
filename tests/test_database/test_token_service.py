import pytest
from pytest_mock import MockFixture
from sqlalchemy.exc import NoReferenceError

from imagesecrets.database.token.services import TokenService


def test_create_token(mocker: MockFixture):
    token_url = mocker.patch(
        "imagesecrets.core.util.main.token_url",
        return_value="test token",
    )
    password_hash = mocker.patch(
        "imagesecrets.core.password.hash_",
        return_value="test hash",
    )

    result = TokenService.create_token()

    token_url.assert_called_once_with()
    password_hash.assert_called_once_with("test token")
    assert result == ("test token", "test hash")


@pytest.mark.asyncio
async def test_service_delete(token_service: TokenService):
    await token_service.delete(user_id=0)

    token_service._session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_service_create(token_service: TokenService):
    await token_service.create(user_id=0, token_hash="test hash")

    token_service._session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_service_get_user_id_ok(
    mocker: MockFixture,
    token_service: TokenService,
    async_iterator,
):
    password_auth = mocker.patch(
        "imagesecrets.core.password.auth",
        return_value=True,
    )

    async_iterator.objs = [("test id", "test hash")]
    token_service._session.stream.return_value = async_iterator

    result = await token_service.get_user_id(token="test token")

    token_service._session.stream.assert_called_once()
    password_auth.assert_called_once_with("test token", "test hash")
    assert result == "test id"


@pytest.mark.asyncio
async def test_service_get_user_id_no_ref(
    token_service: TokenService,
    async_iterator,
):
    async_iterator.objs = []
    token_service._session.stream.return_value = async_iterator

    with pytest.raises(NoReferenceError):
        await token_service.get_user_id(token="test token")

    token_service._session.stream.assert_called_once()


@pytest.mark.asyncio
async def test_service_clear(token_service: TokenService):
    await token_service.clear()

    token_service._session.execute.assert_called_once()
