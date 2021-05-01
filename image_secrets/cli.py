"""Command line interface."""
import re
from typing import Optional

import click

from image_secrets.backend import decode as decode_
from image_secrets.backend import encode as encode_
from image_secrets.backend import regex


def validate_png(_, file: str) -> Optional[str]:
    """Validate that the file has a png extension.

    :param _: Dump the context passed in by click
    :param file: The file to check

    :raises BadParameter: If the pattern does not match

    """
    if re.match(regex.PNG_EXT, file):
        return file
    raise click.BadParameter(f"The file {file!s} is not a .PNG image.")


@click.group()
@click.pass_context
def image_secrets(ctx) -> None:
    """Encode and decode messages into/from images."""


@image_secrets.command(options_metavar="<filename> <message>")
@click.option(
    "--filename",
    type=click.Path(exists=True, resolve_path=True),
    prompt=True,
    callback=validate_png,
    help="the path to the source image, .PNG image is required",
    metavar="<filename>",
)
@click.option(
    "--message",
    type=str,
    prompt=True,
    help="the message to encode",
    metavar="<message>",
)
@click.option(
    "--inplace",
    type=bool,
    default=False,
    show_default=True,
    help="whether the message should be encoded into the original image or not",
    metavar="<bool>",
)
def encode(filename: str, message: str, inplace: bool) -> None:
    """
    \b
    Encode a <message> into a copy of the given <file>.
    Encode inplace if <inplace> is True.

    \f

    :param filename: The filename of the source image, must have a .png extension
    :param message: The text to encode
    :param inplace: Whether the message should be encoded into the given image
        or if a copy of the image should be created, defaults to False

    :raises BadParameter: If the source image is not large enough for the given text

    """
    try:
        filename = encode_.main(filename, message, inplace)
    except ValueError as e:
        raise click.BadParameter(e)
    else:
        click.echo(f"\nEncoded message {message!r} into {filename!r}")
        click.launch(filename, locate=True)


@image_secrets.command(options_metavar="<filename>")
@click.option(
    "--filename",
    type=click.Path(exists=True),
    prompt=True,
    callback=validate_png,
    help="the path to the source image, .PNG image is required",
    metavar="<filename>",
)
def decode(filename: str) -> None:
    """
    Decode a message from <file>.

    \f

    :param filename: The filename of the source image to decode

    :raises BadParameter: If the decoding function did not find any message

    """
    try:
        decoded = decode_.main(filename)
    except StopIteration as e:
        raise click.BadParameter(e)
    else:
        click.echo(f"\nMessage decoded from {filename!s}:\n{decoded!r}")
