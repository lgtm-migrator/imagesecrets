"""Test the module used for decoding."""
from __future__ import annotations

import random as rn
from typing import TYPE_CHECKING

import numpy as np
import pytest

from image_secrets.backend import decode

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


@pytest.mark.parametrize("lsb_n", [1, 2, 3, 4, 5, 6, 7, 8])
def test_prepare_array(random_image_arr: ArrayLike, lsb_n: int) -> None:
    """Test the prepare array function."""
    result = decode.prepare_array(random_image_arr, lsb_n, False)

    assert np.ceil(random_image_arr.size / result.size) == np.ceil(8 / lsb_n)
    assert result.ndim == 1

    np.testing.assert_array_equal(
        np.unpackbits(random_image_arr).reshape(-1, 8)[:, -lsb_n:],
        np.unpackbits(result).reshape(-1, lsb_n),
    )


@pytest.mark.parametrize("lsb_n", [-1, 0, 9, 1000])
def test_prepare_array_raises(lsb_n: int):
    """Test that the prepare array function raises value error if invalid lsb_n arg is passed in."""
    with pytest.raises(ValueError):
        decode.prepare_array(..., lsb_n, ...)


@pytest.mark.parametrize("text", ["", " ", "hello", "987654321", "~!@#$%^&*()_"])
def test_decode_text(text: str) -> None:
    """Test the decode text function."""
    random_noise = "".join(map(chr, (rn.randint(0, 255) for _ in range(1000))))
    ascii_msg = map(ord, f"{text}dlm{random_noise}")

    result = decode.decode_text(np.fromiter(ascii_msg, dtype=np.uint8), "dlm")

    assert not result.endswith("dlm")
    np.testing.assert_string_equal(result, text)


def test_decode_text_raises(
    random_image_arr: ArrayLike,
    test_image_array: ArrayLike,
) -> None:
    """Test that the decode_text function raises StopIteration with wrong input."""
    with pytest.raises(StopIteration):
        decode.decode_text(random_image_arr.ravel(), "fake delimiter")
        decode.decode_text(test_image_array.ravel(), "fake delimiter")
