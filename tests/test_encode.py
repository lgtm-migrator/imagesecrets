"""Test the module used for encoding."""
import functools as fn
from typing import Optional

import numpy as np
import pytest
from numpy.typing import DTypeLike

from image_secrets.backend import encode, util

np.array = fn.partial(np.array, dtype=np.uint8)


@pytest.fixture()
def delimeter_array() -> DTypeLike:
    """Return a delimeter array, string form = 'dlm'."""
    return np.array(
        (
            [0],
            [1],
            [1],
            [0],
            [0],
            [1],
            [0],
            [0],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [0],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
        ),
    )


@pytest.mark.parametrize(
    "binary_text",
    [
        "",
        "111111111111111111111111",
        "000000000000000000000000",
        "010101010101010101010101",
        "0110000100110100" * 30,
    ],
)
def test_encode_message(image_arr, binary_text) -> None:
    """Test the encode_message function.

    :param image_arr: The array with random image data
    :param binary_text: The text to be encoded into the image array

    """
    new_arr = encode.encode_message(
        image_arr.shape,
        image_arr.flatten(),
        binary_text,
        1,
    )

    extracted_bits = ""
    for pixel, bit in zip(new_arr.flat, range(len(binary_text))):
        extracted_bits += bin(pixel)[-1]

    assert binary_text == extracted_bits


def test_encode_limit(image_arr) -> None:
    """Test the the encode function raises a ValueError if the given message is too long.

    :param image_arr: The array with random image data

    """
    with pytest.raises(ValueError):
        encode.encode_message(
            ...,
            image_arr,
            "".join(util.str_to_binary("'long'")) * 1000,
            1,
        )


@pytest.mark.parametrize(
    "message, bits, expected_arr",
    [
        (" ", 1, np.array(([0], [0], [1], [0], [0], [0], [0], [0]))),
        ("A", 1, np.array(([0], [1], [0], [0], [0], [0], [0], [1]))),
        ("1", 1, np.array(([0], [0], [1], [1], [0], [0], [0], [1]))),
        ("22", 2, np.array(([0], [0], [1], [1], [0], [0], [1], [0]) * 2)),
        ("333", 3, np.array(([0], [0], [1], [1], [0], [0], [1], [1]) * 3)),
        ("4444", 4, np.array(([0], [0], [1], [1], [0], [1], [0], [0]) * 4)),
        ("55555", 5, np.array(([0], [0], [1], [1], [0], [1], [0], [1]) * 5)),
        ("666666", 6, np.array(([0], [0], [1], [1], [0], [1], [1], [0]) * 6)),
        ("7777777", 7, np.array(([0], [0], [1], [1], [0], [1], [1], [1]) * 7)),
        ("88888888", 8, np.array(([0], [0], [1], [1], [1], [0], [0], [0]) * 8)),
        ("Z" * 50, 1, np.array(([0], [1], [0], [1], [1], [0], [1], [0]) * 50)),
        ("&" * 50, 5, np.array(([0], [0], [1], [0], [0], [1], [1], [0]) * 50)),
    ],
)
def test_message_bit_array(
    message: str,
    bits: int,
    expected_arr: DTypeLike,
    delimeter_array,
) -> None:
    """Test the prepare message function."""
    expected_arr = np.concatenate((expected_arr, delimeter_array))
    expected_arr.resize(
        (np.ceil(expected_arr.size / bits).astype(int), bits),
        refcheck=False,
    )

    array, length = encode.message_bit_array(message, "dlm", bits)

    # numpy testing for better visual array differences, raises AssertionError same way like assert
    np.testing.assert_array_equal(array, expected_arr)
    assert length == expected_arr.size // bits


__all__ = [
    "test_encode_limit",
    "test_encode_message",
]
