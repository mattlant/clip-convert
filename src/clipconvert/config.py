"""
Configuration file for ClipConvert application.
"""
from pathlib import Path

from clipconvert.version import __version__


APP_NAME = "ClipConvert"
APP_VERSION = __version__
ICON_PATH = Path(__file__).resolve().parent / "assets" / "clip-convert-light.ico"

# GUI Configuration
WINDOW_TITLE = APP_NAME
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400
THEME = "dark"
