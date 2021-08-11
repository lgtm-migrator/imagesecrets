"""Test API response schemas."""
from __future__ import annotations

import pytest

from image_secrets.api import schemas


@pytest.mark.parametrize(
    "key, result",
    [
        ("", ""),
        ("a", "A"),
        ("A", "A"),
        ("camel", "Camel"),
        ("camel_case", "CamelCase"),
    ],
)
def test_pretty_key(key: str, result: str) -> None:
    """Test the pretty_key function."""
    output = schemas.pretty_key(key)

    assert output == result


def test_pretty_key_in_alias() -> None:
    """Test the pretty_key function with a key with knows alias."""
    output = schemas.pretty_key("swagger_url")

    assert output == "SwaggerUI"


def test_info_keys() -> None:
    """Test that ``Info`` fields have correct aliases."""
    properties: dict[str, str] = schemas.Info.schema()["properties"]

    assert properties.get("AppName")
    assert properties.get("SwaggerUI")
    assert properties.get("ReDoc")
    assert properties.get("GitHub")


def test_field_inherit() -> None:
    """Test that the ``Field`` schemas has proper fields."""
    properties: dict[str, str] = schemas.Field.schema()["properties"]

    assert properties.get("detail")


def test_conflict_inherit() -> None:
    """Test that the ``Conflict`` schemas has proper fields."""
    properties: dict[str, str] = schemas.Conflict.schema()["properties"]

    assert properties.get("detail")
    assert properties.get("field")
