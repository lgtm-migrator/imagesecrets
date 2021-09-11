def test_get(api_client, api_settings) -> None:
    """Test get request on the home route."""
    response = api_client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "AppName": api_settings.app_name,
        "SwaggerUI": api_settings.swagger_url,
        "ReDoc": api_settings.redoc_url,
        "GitHub": api_settings.repository_url,
    }
