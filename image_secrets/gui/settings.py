"""Settings for GUI."""
import qdarkstyle


def light_stylesheet() -> str:
    """Return the stylesheet to be associated with light mode."""
    return ""


def dark_stylesheet() -> str:
    """Return the stylesheet to be associated with dark mode."""
    return qdarkstyle.load_stylesheet(qt_api="PyQt5")
