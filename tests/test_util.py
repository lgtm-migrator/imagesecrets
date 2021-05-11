"""Test the util module."""
from __future__ import annotations

import functools as fn
import string
from typing import TYPE_CHECKING

import numpy as np
import pytest

from image_secrets.backend import util

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


np.array = fn.partial(np.array, dtype=np.uint8)  # no need to repeat dtype again


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
    expected_arr: ArrayLike,
    delimeter_array,
) -> None:
    """Test the prepare message function."""
    expected_arr = np.concatenate((expected_arr, delimeter_array))
    expected_arr.resize(
        (np.ceil(expected_arr.size / bits).astype(int), bits),
        refcheck=False,
    )

    array, length = util.message_bit_array(message, "dlm", bits)

    # numpy testing for better visual array differences, raises AssertionError same way like assert
    np.testing.assert_array_equal(array, expected_arr)
    assert length == expected_arr.size // bits


@pytest.mark.parametrize(
    "bytes_",
    [
        b"",
        b"qwerty",
        b"123456789",
        b"~!@#$%^&**()",
    ],
)
def test_read_image_bytes(bytes_: bytes) -> None:
    """Test the read_image_bytes function.

    :param bytes_: Bytes to read

    """
    num = np.random.randint(0, 10)
    assert util.read_image_bytes(bytes_).read(num) == bytes_[:num]


def test_image_data(test_image_path) -> None:
    """Test the image_data function."""
    shape, arr = util.image_data(test_image_path)

    assert arr.ndim == 3
    assert arr.dtype == np.uint8
    assert arr.max() <= 255
    assert arr.min() >= 0

    assert shape[-1] == 3


@pytest.mark.parametrize("length", [16, 64, 33, 0, -8, 101])
def test_token_hex(length) -> None:
    """Test the token_hex function."""
    char_set = {i for i in (string.ascii_lowercase + string.digits)}

    token = util.token_hex(length)

    length = abs(length)

    assert len(token) == length if length % 2 == 0 else length + 1
    assert all(i in char_set for i in token)


__all__ = [
    "test_message_bit_array",
]
