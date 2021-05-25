"""Test the decode router with authenticated user."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from pytest_mock import MockFixture

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

    from image_secrets.backend.database.user.models import User

URL = "/decode"


def test_get_empty(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
) -> None:
    """Test the get request with no stored images."""
    token = auth_token[1]
    response = api_client.get(
        URL,
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
    )

    response.raise_for_status()
    assert response.status_code == 200
    assert response.reason == "OK"
    json_ = response.json()
    assert isinstance(json_, list)
    assert not json_
    assert response.headers["content-length"] == "2"


def test_get(api_client: TestClient, auth_token: tuple[User, dict[str, str]]) -> None:
    """Test the get request."""
    token = auth_token[1]
    user = auth_token[0]

    from image_secrets.backend.database.image.models import DecodedImage

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        DecodedImage.create(
            filename="filename",
            image_name="image_name",
            message="message",
            delimiter="delimiter",
            owner_id=user.id,
        ),
    )

    response = api_client.get(
        URL,
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
    )

    response.raise_for_status()
    assert response.status_code == 200
    assert response.reason == "OK"
    json_ = response.json()
    assert isinstance(json_, list)
    image = json_[0]
    assert image["image_name"] == "image_name"
    assert image["message"] == "message"
    assert image["delimiter"] == "delimiter"
    assert image["lsb_amount"] == 1


@pytest.mark.parametrize(
    "delimiter, lsb_n",
    [
        ("dlm1", 1),
        ("dlm2", 2),
        ("dlm3", 3),
        ("dlm5", 4),
        ("dlm5", 5),
        ("dlm6", 6),
        ("dlm7", 7),
        ("dlm8", 8),
    ],
)
def test_post(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
    api_image_file,
    test_image_path: Path,
    mocker: MockFixture,
    delimiter: str,
    lsb_n: int,
) -> None:
    """Test a successful post request."""
    buffer = api_image_file["file"][1]

    decode_api = mocker.patch(
        "image_secrets.backend.decode.api",
        return_value=("decoded>test", test_image_path),
    )

    token = auth_token[1]
    response = api_client.post(
        URL,
        files=api_image_file,
        data={"custom-delimiter": delimiter, "least-significant-bit-amount": lsb_n},
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
    )

    decode_api.assert_called_once_with(
        image_data=buffer,
        delimiter=delimiter,
        lsb_n=lsb_n,
        reverse=False,
    )

    response.raise_for_status()
    assert response.status_code == 201
    assert response.reason == "Created"
    json_ = response.json()
    assert json_["image_name"] == "test.png"
    assert json_["message"] == "decoded>test"
    assert json_["delimiter"] == delimiter
    assert json_["lsb_amount"] == lsb_n


def test_post_200(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
    mocker: MockFixture,
    test_image_path: Path,
    api_image_file,
) -> None:
    """Test a post request with valid request but no decoded result."""
    buffer = api_image_file["file"][1]

    decode_api = mocker.patch(
        "image_secrets.backend.decode.api",
    )
    decode_api.side_effect = StopIteration("test exception")

    token = auth_token[1]
    response = api_client.post(
        URL,
        files=api_image_file,
        data={"custom-delimiter": "delimiter", "least-significant-bit-amount": 1},
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
    )

    decode_api.assert_called_once_with(
        image_data=buffer,
        delimiter="delimiter",
        lsb_n=1,
        reverse=False,
    )

    response.raise_for_status()
    assert response.status_code == 200
    assert response.reason == "OK"
    assert response.json()["detail"] == "test exception"
    headers = response.headers
    assert headers["custom-delimiter"] == "delimiter"
    assert headers["least-significant-bit-amount"] == repr(1)


def test_post_415(
    api_client: TestClient,
    auth_token: tuple[User, dict[str, str]],
) -> None:
    """Test a post request with invalid media type."""
    token = auth_token[1]
    response = api_client.post(
        URL,
        files={
            "file": (Path(__file__).name, open(__file__).read(), "image/png"),
        },
        headers={
            "authorization": f'{token["token_type"].capitalize()} {token["access_token"]}',
        },
    )

    assert response.status_code == 415
    assert response.reason == "Unsupported Media Type"
    assert response.json()["detail"] == "only .png images are supported"
