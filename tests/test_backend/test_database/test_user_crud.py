"""Test the CRUD module for users."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets.backend.database.user import crud

if TYPE_CHECKING:
    from pytest_mock import MockFixture


def test_get_ok() -> None:
    """Test successful get function call."""


def test_get_id_ok() -> None:
    """Test successful get_id function call."""


def test_create_ok() -> None:
    """Test successful create function call."""


def test_delete_ok() -> None:
    """Test successful delete function call."""


def test_update_no_password_hash() -> None:
    """Test successful update function call without a password hash."""


def test_update_with_password_hash() -> None:
    """Test successful update function call with a password hash."""


def test_authenticate_ok() -> None:
    """Test successful authenticate function call."""


def test_authenticate_fail_password_match() -> None:
    """Test failing authenticate function call due to not matching password and its hash."""


def test_authenticate_fail_no_db_entry() -> None:
    """Test failing authenticate function call due to inability to find database user entry."""
