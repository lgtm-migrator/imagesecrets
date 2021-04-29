"""Test the encode module."""
from pathlib import Path

import pytest
import numpy as np

from src.backend import encode


@pytest.fixture()
def image_arr():
    return encode.image_array(Path("test.png").absolute())


@pytest.mark.parametrize(
    "text, result",
    [
        ("", ""),
        ("123", "001100010011001000110011"),
        ("abc", "011000010110001001100011"),
        ("1a*", "001100010110000100101010"),
        ("1 a", "001100010010000001100001"),
        (" 1a ", "00100000001100010110000100100000"),
        (".", "00101110"),
        (
            "long_text... ",
            "01101100011011110110111001100111010111110111010001100101011110000111010000101110001011100010111000100000",
        ),
    ],
)
def test_str_into_bin_array(text, result):
    arr = encode.str_into_bin_array(text)
    data = "".join(
        (format(i, "b").zfill(8)[-1] for i, _ in zip(arr.flatten(), range(len(result))))
    )
    assert data == result
