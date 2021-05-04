"""Test that the menu bar works properly.

Clicking on menu bar actions hard to accomplish, that's why their events are just manually triggered.
Refer to this github issue for more information: https://github.com/pytest-dev/pytest-qt/issues/195

"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from image_secrets.gui.interface import ImageSecretsWindow
from image_secrets.gui.settings import DARK_STYLESHEET, LIGHT_STYLESHEET

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QMainWindow
    from pytestqt.qtbot import QtBot


@pytest.fixture()
def application(qtbot: QtBot) -> QMainWindow:
    """Return the main window."""
    test_app = ImageSecretsWindow()
    qtbot.addWidget(test_app)
    return test_app


@pytest.mark.parametrize(
    "action, index",
    [
        ("action_decode", 2),
        ("action_encode", 1),
        ("action_home", 0),
    ],
)
def test_switch_action(
    application: QMainWindow,
    action: str,
    index: int,
) -> None:
    """Test that each ``QAction`` responsible for switching widgets on the main stacked_widget works.

    :param application: The application to test
    :param action: QAction pointer
    :param index: Expected index after clicking the action

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
def test_theme_action(
    application: QMainWindow,
    action: str,
    sheet: str,
) -> None:
    """Test that the actions that change application themes work.

    End is at the 100th because some sheets can be bigger than allowed by env variables
    :param application: The application to test
    :param action: QAction pointer
    :param sheet: Expected stylesheet after clicking the action

    """
    action = getattr(application.ui, action)
    action.trigger()
    assert application.main_win.styleSheet()[:100] == sheet
