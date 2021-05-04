"""Execute the Application Programming Interface"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn

from image_secrets.api.interface import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
