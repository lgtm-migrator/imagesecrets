import re
from pathlib import Path

import click

from backend import encode as enc
from backend import decode as dec
from backend.regex import PNG_EXT


def validate_png(_, file: str):
    """Validate that the file has as png extension.

    :param _: Dump the context passed in by click
    :param file: The file to check

    """
    if re.match(PNG_EXT, file):
        return file
    raise click.BadParameter("PNG is required.")


@click.group()
@click.pass_context
def cli(ctx):
    """CLI tool used for encoding and decoding messages into/from images."""


@cli.command()
@click.option(
    "--filename",
    type=click.Path(exists=True, resolve_path=True),
    prompt=True,
    callback=validate_png,
)
@click.option("--message", "text", type=str, prompt=True)
@click.option("--inplace", type=bool, default=False, show_default=True)
def encode(filename: str, text: str, inplace: bool):
    """Encode image command.

    :param filename: The filename of the source image, must have a .png extension
    :param text: The text to encode
    :param inplace: Whether the message should be encoded into the given image
        or if a copy of the image should be created, defaults to False

    """
    try:
        click.echo(enc.main(Path(filename).absolute(), text, inplace))
    except ValueError as e:
        click.echo(e)


@cli.command()
@click.option("--filename", type=click.Path(exists=True), prompt=True)
def decode(filename):
    """Decode image"""
    click.echo(dec.text(filename))


if __name__ == "__main__":
    cli()
