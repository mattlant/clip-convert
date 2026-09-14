"""Tests for application identity and package-relative resources."""
import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from clipconvert import config
from clipconvert.conversion_service import ConversionService
from clipconvert.main_window import MainWindow
from clipconvert.version import __version__


class TestApplicationIdentity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qt_app = QApplication.instance() or QApplication([])

    def test_version_is_authoritative_for_runtime_and_project_metadata(self):
        self.assertEqual(__version__, "1.0.0")
        self.assertEqual(config.APP_VERSION, __version__)
        self.assertEqual(importlib.metadata.version("clipconvert"), __version__)

    def test_main_window_exposes_identity_and_icon(self):
        service = MagicMock(spec=ConversionService)
        window = MainWindow(service)
        self.addCleanup(window.close)

        self.assertEqual(window.windowTitle(), "ClipConvert")
        self.assertEqual(window._version_label.text(), "ClipConvert 1.0.0")
        self.assertEqual(window._version_label.focusPolicy(), Qt.NoFocus)
        self.assertIn("#888888", window._version_label.styleSheet())
        self.assertIs(window.centralWidget().layout().itemAt(2).widget(), window._version_label)
        self.assertFalse(window.windowIcon().isNull())

    def test_application_uses_identity_and_icon_outside_repository_root(self):
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                source_root = Path(__file__).resolve().parents[1]
                environment = os.environ.copy()
                environment["PYTHONPATH"] = str(source_root / "src")
                environment["QT_QPA_PLATFORM"] = "offscreen"
                result = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        (
                            "from clipconvert.main import ClipConvertApp; "
                            "app = ClipConvertApp(); "
                            "print(app._app.applicationName()); "
                            "print(app._app.applicationVersion()); "
                            "print(app._app.windowIcon().isNull())"
                        ),
                    ],
                    cwd=temp_dir,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=True,
                )

                self.assertEqual(result.stdout.splitlines(), ["ClipConvert", "1.0.0", "False"])
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
