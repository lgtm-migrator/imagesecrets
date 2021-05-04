"""Test the interface module."""
import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from image_secrets.api.interface import app

client = TestClient(app)


@pytest.mark.parametrize(
    "route",
    [
        "",
        "home",
    ],
)
def test_home(route: str):
    response = client.get(route)
    assert response.status_code == 200
    assert response.json() == {"home": "ImageSecrets Home Page"}


def test_decode():
    response = client.post("/decode", data="F:/Luky/Hry/chart.png")

    assert response.status_code == 200
    assert response == {"home": "ImageSecrets Home Page"}
