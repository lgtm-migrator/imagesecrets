"""Test the encode module."""
from pathlib import Path

import pytest
import numpy as np

from src.backend import encode


@pytest.fixture()
def image_arr():
    return encode.image_array(Path("test.png").absolute())


@pytest.mark.parametrize(
    "text",
    [
        "",
        "123",
        "abc",
        "1a*",
        "1 a",
        " 1a ",
        ".",
        "qwertyasdf...",
        "\\\\\\",
        "~!@#$%$^&*(*)+",
    ],
)
def test_str_into_bin_array(text):
    result = "".join(
        map(
            lambda char: format(char, "b").zfill(8),
            bytearray(text, encoding="utf-8"),
        )
    )

    arr = encode.str_into_bin_array(text)
    data = "".join(
        (format(i, "b").zfill(8)[-1] for i, _ in zip(arr.flatten(), range(len(result))))
    )

    assert data == result


@pytest.mark.parametrize(
    "text",
    [
        "",
        "123",
        "abc",
        "1a*",
        "1 a",
        " 1a ",
        ".",
        "qwertyasdf... ",
        "\\\\\\",
        "~!@#$%$^&*(*)+",
    ],
)
def test_encode_message(image_arr, text):
    new_arr = encode.encode_message(image_arr, text)
    extracted_text = ""
    for rgb_vals, _ in zip(new_arr.reshape(-1, 8), range(len(text))):
        binary = (bin(num)[-1] for num in rgb_vals)
        char = chr(int("".join(binary), base=2))
        extracted_text += char

    assert text == extracted_text
