import re
from pathlib import Path
from typing import Optional

import click

from image_secrets.backend import decode as decode_
from image_secrets.backend import encode as encode_
from image_secrets.backend import regex


def validate_png(_, file: str) -> Optional[str]:
    """Validate that the file has as png extension.

    :param _: Dump the context passed in by click
    :param file: The file to check

    :raises BadParameter: If the pattern does not match

    """
    if re.match(regex.PNG_EXT, file):
        return file
    raise click.BadParameter(f"The {file!s} is not a .PNG image.")


@click.group()
@click.pass_context
def image_secrets(ctx):
    """CLI tool used for encoding and decoding messages into/from images."""


@image_secrets.command()
@click.option(
    "--filename",
    type=click.Path(exists=True, resolve_path=True),
    prompt=True,
    callback=validate_png,
)
@click.option("--message", "message", type=str, prompt=True)
@click.option("--inplace", type=bool, default=False, show_default=True)
def encode(filename: str, text: str, inplace: bool):
    """Encode image command.

    :param filename: The filename of the source image, must have a .png extension
    :param text: The text to encode
    :param inplace: Whether the message should be encoded into the given image
        or if a copy of the image should be created, defaults to False

    :raises BadParameter: If the source image is not large enough for the given text

    """
    try:
        filename = encode_.main(Path(filename), text, inplace)
    except ValueError as e:
        raise click.BadParameter from e
    else:
        click.echo(
            f"""\nEncoded message {text!r} into
            {encode_.main(Path(filename), text, inplace)!r}""",
        )


@image_secrets.command()
@click.option("--filename", type=click.Path(exists=True), prompt=True)
def decode(filename):
    """Decode image command.

    :param filename: The filename of the source image to decode

    :raises BadParameter: If the decoding function did not find any message

    """
    try:
        decoded = decode_.main(filename)
    except StopIteration as e:
        raise click.BadParameter from e
    else:
        click.echo(f"Message decoded from {filename!s}:\n{decoded!r}")
