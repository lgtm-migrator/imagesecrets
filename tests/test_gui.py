"""Test the gui package."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets.gui.interface import ImageSecretsWindow
from image_secrets.gui.settings import DARK_STYLESHEET, LIGHT_STYLESHEET

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow


@pytest.fixture()
def application(qtbot) -> QMainWindow:
    """Return the main window."""
    test_app = ImageSecretsWindow()
    qtbot.addWidget(test_app)
    return test_app


############
# Menu Bar #
############


@pytest.mark.parametrize(
    "action, index",
    [
        ("action_decode", 2),
        ("action_encode", 1),
        ("action_home", 0),
    ],
)
def test_switch_action(application: QMainWindow, action: str, index: int) -> None:
    """Test that each ``QAction`` responsible for switching widgets on the main stacked_widget works.

    :param application: The application to test
    :param action: The action which is going to be clicked
    :param index: The expected index after clicking the action

    """
    action = getattr(application.ui, action)
    action.trigger()
    assert application.ui.stacked_widget.currentIndex() == index


def test_exit_action(application: QMainWindow) -> None:
    """Test that the exit action closes the window."""
    application.ui.action_exit.trigger()
    assert application.close() is True


@pytest.mark.parametrize(
    "action, sheet",
    [
        ("action_light", LIGHT_STYLESHEET[:100]),
        ("action_dark", DARK_STYLESHEET[:100]),
    ],
)
def test_theme_action(application: QMainWindow, action: str, sheet: str) -> None:
    """Test that the actions that change application themes work.

    End is at the 100th because some sheets can be bigger than allowed by env variables

    :param application: The application to test
    :param action: The action which is going to be clicked
    :param sheet: The expected stylesheet after clicking the action

    """
    print(sheet, "ls")
    action = getattr(application.ui, action)
    action.trigger()
    assert application.main_win.styleSheet()[:100] == sheet
