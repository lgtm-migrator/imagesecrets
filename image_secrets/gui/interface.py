"""Graphical user interface."""
from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from PyQt5 import QtCore, QtGui, QtWidgets

from image_secrets.gui import buttons
from image_secrets.gui.events import ImageSecretsEvents
from image_secrets.gui.static.qt_designer.output.main import Ui_ImageSecrets
from image_secrets.settings import ICON

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QApplication


def image_secrets() -> None:
    """Execute the main window."""
    QtCore.QCoreApplication.setApplicationName("ImageSecrets")
    app = QtWidgets.QApplication(sys.argv)

    main_window = ImageSecretsWindow()
    tray_menu(app, main_window)

    main_window.show()
    app.exec()


def tray_menu(app: QApplication, main_window: ImageSecretsWindow) -> None:
    """Setup a tray icon for the ImageSecretsWindow.

    :param app: The currently running ``QApplication`` instance
    :param main_window: The window which will be shown

    """
    tray_icon = QtWidgets.QSystemTrayIcon(
        QtGui.QIcon(str(ICON)),
        app,
    )
    tray_icon.setToolTip("ImageSecrets")

    # inherit main window to follow current style sheet
    menu = QtWidgets.QMenu(main_window.main_win)

    decode_option = menu.addAction("Decode")
    decode_option.triggered.connect(
        lambda: main_window.ui.stacked_widget.setCurrentIndex(2),
    )

    encode_option = menu.addAction("Encode")
    encode_option.triggered.connect(
        lambda: main_window.ui.stacked_widget.setCurrentIndex(1),
    )

    exit_action = menu.addAction("Exit ImageSecrets")
    exit_action.triggered.connect(
        lambda: main_window.ui.stacked_widget.setCurrentIndex(quit),
    )

    tray_icon.setContextMenu(menu)
    tray_icon.show()


class ImageSecretsWindow(QtWidgets.QMainWindow):
    """Main GUI window for ImageSecrets."""

    def __init__(self, parent=None) -> None:
        """Construct the main window."""
        super().__init__(parent)

        self.main_win = QtWidgets.QMainWindow()
        self.main_win.setWindowIcon(QtGui.QIcon(str(ICON)))
        self.main_win.setWindowTitle("ImageSecrets")
        self.main_win.setMinimumSize(470, 350)

        self.ui = Ui_ImageSecrets()
        self.ui.setupUi(self.main_win)

        self.events = ImageSecretsEvents(self)

        buttons.setup(self)
        self.ui.action_dark.trigger()  # set dark theme

    def __repr__(self) -> str:
        """Provide information about this class."""
        return f"{self.__class__.__qualname__}()"

    def show(self) -> None:
        """Show the main window."""
        self.center()
        self.ui.stacked_widget.setCurrentIndex(0)
        self.main_win.show()

    def center(self) -> None:
        """Center the main window."""
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


__all__ = [
    "ImageSecretsWindow",
    "image_secrets",
    "tray_menu",
]
