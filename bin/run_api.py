"""Execute the Application Programming Interface"""
import sys
from pathlib import Path

import uvicorn

from image_secrets.api import interface

sys.path.append(str(Path(__file__).parent.parent))


if __name__ == "__main__":
    uvicorn.run(interface.app, host="0.0.0.0", port=80)
