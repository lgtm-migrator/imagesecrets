"""Test the CRUD module for token."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets.backend.database.user import crud

if TYPE_CHECKING:
    from pytest_mock import MockFixture


def test_create() -> None:
    """Test the create function."""


def test_get_owner_id_ok() -> None:
    """Test successful get_owner_id function call."""


def test_get_owner_id_fail() -> None:
    """Test failing get_owner_id function call."""
