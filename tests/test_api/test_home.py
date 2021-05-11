"""Test the interface module."""
import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from image_secrets.api.interface import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"app-name": "ImageSecrets"}


__all__ = [
    "client",
    "test_home",
]
