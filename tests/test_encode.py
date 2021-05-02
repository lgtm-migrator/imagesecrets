"""Test the module used for encoding."""
import numpy as np
import pytest

from image_secrets.backend import encode, util


@pytest.fixture()
def image_arr():
    """Return array containing data about a random image."""
    return np.random.randint(0, 255, size=(256, 3), dtype=np.uint8)


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
    new_arr = encode.encode_message(image_arr.shape, image_arr.flatten(), binary_text)

    extracted_bits = ""
    for pixel, bit in zip(new_arr.flat, range(len(binary_text))):
        extracted_bits += bin(pixel)[-1]

    assert binary_text == extracted_bits


def test_encode_limit(image_arr) -> None:
    """Test the the encode function raises a ValueError if the given message is too long.

    :param image_arr: The array with random image data

    """
    with pytest.raises(ValueError):
        encode.encode_message(..., image_arr, util.str_to_binary("'long'") * 1000)


__all__ = [
    "image_arr",
    "test_encode_limit",
    "test_encode_message",
]
