"""Execute the command line interface."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from image_secrets import cli

if __name__ == "__main__":
    cli.image_secrets()
