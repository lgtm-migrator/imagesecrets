import pytest
from pytest_mock import MockFixture
from sqlalchemy.sql.elements import BinaryExpression

from imagesecrets.schemas import UserCreate


@pytest.mark.parametrize(
    "column, value",
    [
        ("id", "test_id"),
        ("username", "test_username"),
        ("email", "test_email"),
    ],
)
def test_dbidentifier_to_sqlalchemy_str(column: str, value: str):
    from imagesecrets.database.user.services import DBIdentifier

    result = DBIdentifier(column=column, value=value).to_sqlalchemy()

    assert isinstance(result, BinaryExpression)


@pytest.mark.asyncio
async def test_service_get(mocker, user_service):
    from imagesecrets.database.user.models import User
    from imagesecrets.database.user.services import DBIdentifier

    return_value = mocker.Mock()
    return_value.scalar_one = mocker.Mock(return_value="get called")
    user_service._session.execute.return_value = return_value

    result = await user_service.get(
        DBIdentifier(User.username, "test_username"),
    )

    user_service._session.execute.assert_called_once()
    return_value.scalar_one.assert_called_once_with()
    assert result == "get called"


@pytest.mark.asyncio
async def test_service_get_id(mocker, user_service):
    from imagesecrets.database.user.models import User
    from imagesecrets.database.user.services import DBIdentifier

    return_value = mocker.Mock()
    return_value.scalar_one = mocker.Mock(return_value="get_id called")
    user_service._session.execute.return_value = return_value

    result = await user_service.get_id(
        DBIdentifier(User.username, "test_username"),
    )

    user_service._session.execute.assert_called_once()
    return_value.scalar_one.assert_called_once_with()
    assert result == "get_id called"


@pytest.mark.asyncio
async def test_service_create(user_service):
    from imagesecrets.database.user.models import User

    result = await user_service.create(
        UserCreate(
            username="test_username",
            email="test_email@email.com",
            password="test_password",
        ),
    )

    user_service._session.add.assert_called_once_with(result)
    assert isinstance(result, User)


@pytest.mark.asyncio
async def test_service_delete(user_service):
    await user_service.delete(user_id=0)

    user_service._session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_service_update(mocker: MockFixture, user_service):
    from imagesecrets.database.user.models import User
    from imagesecrets.database.user.services import DBIdentifier

    service_get = mocker.patch(
        "imagesecrets.database.user.services.UserService.get",
    )

    await user_service.update(user_id=0, username="test username")

    user_service._session.execute.assert_called_once()
    service_get.assert_called_once_with(DBIdentifier(column=User.id, value=0))


@pytest.mark.asyncio
async def test_service_update_password(mocker: MockFixture, user_service):
    from imagesecrets.database.user.models import User
    from imagesecrets.database.user.services import DBIdentifier

    password_hash = mocker.patch("imagesecrets.core.password.hash_")
    service_get = mocker.patch(
        "imagesecrets.database.user.services.UserService.get",
    )

    await user_service.update(user_id=0, password_hash="123")

    password_hash.assert_called_once_with("123")
    user_service._session.execute.assert_called_once()
    service_get.assert_called_once_with(DBIdentifier(column=User.id, value=0))


@pytest.mark.asyncio
async def test_service_authenticate_no_result(
    mocker: MockFixture,
    user_service,
):
    return_value = mocker.Mock()
    return_value.scalar_one_or_none = mocker.Mock(return_value=None)
    user_service._session.execute.return_value = return_value

    result = await user_service.authenticate(
        username="test username",
        password_="test password",
    )

    user_service._session.execute.assert_called_once()
    return_value.scalar_one_or_none.assert_called_once_with()
    assert result is False


@pytest.mark.asyncio
async def test_service_authenticate_invalid(mocker: MockFixture, user_service):
    return_value = mocker.Mock()
    return_value.scalar_one_or_none = mocker.Mock(return_value="hashed")
    user_service._session.execute.return_value = return_value

    mocker.patch("imagesecrets.core.password.auth", return_value=True)

    result = await user_service.authenticate(
        username="test username",
        password_="test password",
    )

    user_service._session.execute.assert_called_once()
    return_value.scalar_one_or_none.assert_called_once_with()
    assert result is True
