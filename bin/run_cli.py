"""Execute the command line interface."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from image_secrets.cli import interface

if __name__ == "__main__":
    interface.image_secrets()
