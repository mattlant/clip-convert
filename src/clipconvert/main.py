"""
Main application entry point for ClipConvert.
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from clipconvert.clipboard_service import ClipboardService
from clipconvert.conversion_service import ConversionService
from clipconvert.initialization import initialize_converters
from clipconvert.main_window import MainWindow
from clipconvert import config


class ClipConvertApp:
    """Main application class."""

    def __init__(self):
        self._app = QApplication(sys.argv)
        self._app.setApplicationName(config.APP_NAME)
        self._app.setApplicationVersion(config.APP_VERSION)
        self._app.setWindowIcon(QIcon(str(config.ICON_PATH)))
        self._setup_services()
        self._setup_main_window()

    def _setup_services(self):
        """Initialize all services."""
        clipboard = self._app.clipboard()
        self._clipboard_service = ClipboardService(clipboard)
        self._converter_registry = initialize_converters()
        self._conversion_service = ConversionService(
            self._clipboard_service,
            self._converter_registry
        )

    def _setup_main_window(self):
        """Create and configure the main window."""
        self._main_window = MainWindow(self._conversion_service)
        self._main_window.show()

    def run(self) -> int:
        """
        Run the application.
        Returns:
            Exit code
        """
        return self._app.exec()


def main():
    """Main entry point."""
    app = ClipConvertApp()

    sys.exit(app.run())


if __name__ == "__main__":
    main()

