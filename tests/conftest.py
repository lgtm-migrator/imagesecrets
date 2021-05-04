"""Session wide fixtures."""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

from image_secrets.gui.interface import ImageSecretsWindow

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow


@pytest.fixture(scope="session")
def image_arr():
    """Return array containing data about a random image."""
    return np.random.randint(0, 255, size=(256, 3), dtype=np.uint8)


@pytest.fixture()
def application(qtbot) -> QMainWindow:
    """Return the main window."""
    test_app = ImageSecretsWindow()
    qtbot.addWidget(test_app)
    return test_app
