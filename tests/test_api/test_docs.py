"""Test OpenAPI API documentation."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from pytest_mock import MockFixture


def test_swagger(api_client: TestClient, mocker: MockFixture, api_settings) -> None:
    """Test the get request on the home route."""
    swagger = mocker.patch(
        "fastapi.openapi.docs.get_swagger_ui_html",
        return_value="test_swagger",
    )

    response = api_client.get("/docs")

    swagger.assert_called_once_with(
        openapi_url="/openapi.json",
        title=api_settings.app_name,
        swagger_favicon_url=api_settings.icon_url,
    )
    response.raise_for_status()
    assert response.status_code == 200
    assert response.json() == "test_swagger"


def test_redoc(api_client: TestClient, mocker: MockFixture, api_settings) -> None:
    """Test the get request on the home route."""
    redoc = mocker.patch(
        "fastapi.openapi.docs.get_redoc_html",
        return_value="test_redoc",
    )

    response = api_client.get("/redoc")

    redoc.assert_called_once_with(
        openapi_url="/openapi.json",
        title=api_settings.app_name,
        redoc_favicon_url=api_settings.icon_url,
    )
    response.raise_for_status()
    assert response.status_code == 200
    assert response.json() == "test_redoc"
