"""Focused tests for main-window conversion orchestration."""
import unittest
from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QApplication, QMessageBox

from clipconvert.base_converter import BaseConverter
from clipconvert.conversion_service import ConversionService
from clipconvert.main_window import MainWindow


class MockConverter(BaseConverter):
    @property
    def display_text(self):
        return "Test"

    @property
    def supported_mimetype(self):
        return "text/html"

    def convert(self, content):
        return content


class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qt_app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.service = MagicMock(spec=ConversionService)
        self.converter = MockConverter()
        self.service.get_available_converters.return_value = [self.converter]
        self.service.convert.return_value = "| Name | Value |\n| A | 1 |\n"
        self.window = MainWindow(self.service)
        self.addCleanup(self.window.close)

    @patch("clipconvert.main_window.QMessageBox.question")
    def test_displays_before_prompt_and_copies_accepted_result(self, question):
        events = []
        question.return_value = QMessageBox.StandardButton.Yes
        question.side_effect = lambda *args: events.append(
            ("prompt", self.window._results_text.toPlainText())
        ) or QMessageBox.StandardButton.Yes
        self.service.copy_to_clipboard.side_effect = lambda text: events.append(
            ("copy", text)
        )

        self.window._on_convert_clicked()

        self.assertEqual(events[0], ("prompt", "| Name | Value |\n| A | 1 |\n"))
        self.assertEqual(
            events[1],
            ("copy", "| Name | Value |\n| --- | --- |\n| A | 1 |\n"),
        )
        self.assertEqual(self.window._results_text.toPlainText(), events[1][1])

    @patch("clipconvert.main_window.QMessageBox.question")
    def test_copies_unchanged_result_when_declined(self, question):
        question.return_value = QMessageBox.StandardButton.No

        self.window._on_convert_clicked()

        self.service.copy_to_clipboard.assert_called_once_with(
            "| Name | Value |\n| A | 1 |\n"
        )
        self.assertEqual(self.window._results_text.toPlainText(), "| Name | Value |\n| A | 1 |\n")


if __name__ == "__main__":
    unittest.main()
