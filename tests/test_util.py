"""Test the util module."""

import pytest

from image_secrets.backend import util


@pytest.mark.parametrize(
    "string, expected",
    [
        ("", ""),
        ("0", "00110000"),
        ("a", "01100001"),
        ("qwerty", "011100010111011101100101011100100111010001111001"),
        ("!@#$%^&", "00100001010000000010001100100100001001010101111000100110"),
        (" - ", "001000000010110100100000"),
        ("\\", "01011100"),
        ([(i * 100) for i in ("asdf", "01100001011100110110010001100110")]),
    ],
)
def test_str_to_binary(string: str, expected: str) -> None:
    """Test the str_to_binary_ function.

    :param string: The string to turn into binary
    :param expected: The expected result

    """
    assert "".join(util.str_to_binary(string)) == expected


__all__ = [
    "test_str_to_binary",
]
