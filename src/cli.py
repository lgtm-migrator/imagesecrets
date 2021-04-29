import re
from pathlib import Path

import click

from backend import encode as enc
from backend import decode as dec
from backend.regex import PNG_EXT


def validate_png(_, file: str):
    if re.match(PNG_EXT, file):
        return file
    raise click.BadParameter("PNG is required.")


@click.group()
@click.pass_context
def cli(ctx):
    """CLI tool used for encoding and decoding messages from images."""


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
    """Encode image"""
    click.echo(enc.main(Path(filename).absolute(), text, inplace))


@cli.command()
@click.option("--filename", type=click.Path(exists=True), prompt=True)
def decode(filename):
    """Decode image"""
    click.echo(dec.text(filename))


if __name__ == "__main__":
    cli()
