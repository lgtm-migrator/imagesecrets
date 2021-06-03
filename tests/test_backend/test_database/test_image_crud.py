"""Test the CRUD module for images."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets.backend.database.user import crud

if TYPE_CHECKING:
    from pytest_mock import MockFixture


def test_create_decoded() -> None:
    """Test the create_decoded function."""


def test_create_encoded() -> None:
    """Test the create_encoded function."""
