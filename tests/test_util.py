"""Test the util module."""

import pytest

from image_secrets.backend import util


@pytest.mark.parametrize(
    "string, result",
    [
        ("", ""),
        ("0", "00110000"),
        ("a", "01100001"),
        ("qwerty", "011100010111011101100101011100100111010001111001"),
        ("!@#$%^&", "00100001010000000010001100100100001001010101111000100110"),
        (" - ", "001000000010110100100000"),
        ("\\", "01011100"),
        ("asdf" * 100, "01100001011100110110010001100110" * 100),
    ],
)
def test_str_to_binary(string: str, result: str) -> None:
    """Test the str_to_binary_ function.

    :param string: The string to turn into binary
    :param result: The expected result

    """
    assert util.str_to_binary(string) == result


@pytest.mark.parametrize(
    "binary, result",
    [
        ("01100001", "a"),
        ("01100010", "b"),
        ("00110001", "1"),
        ("00110000", "0"),
        ("00101010", "*"),
        ("01111110", "~"),
        ("01011100", "\\"),
    ],
)
def test_binary_to_char(binary: str, result: str) -> None:
    """Test binary_to_char function.

    :param binary: The character in its' binary representation
    :param result: The expected result

    """
    assert util.binary_to_char(binary) == result
