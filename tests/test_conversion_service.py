"""
Unit tests for conversion service.
"""
import unittest
from unittest.mock import Mock, MagicMock
from clipconvert.conversion_service import ConversionService
from clipconvert.base_converter import BaseConverter


class MockConverter(BaseConverter):
    """Mock converter for testing."""

    def __init__(self, display_text: str, mimetype: str):
        self._display_text = display_text
        self._mimetype = mimetype

    @property
    def display_text(self) -> str:
        return self._display_text

    @property
    def supported_mimetype(self) -> str:
        return self._mimetype

    def convert(self, content: str) -> str:
        return f"# {content}"


class TestConversionService(unittest.TestCase):
    """Test cases for ConversionService."""

    def setUp(self):
        """Set up test fixtures."""
        self.clipboard_service = Mock()
        self.converter_registry = Mock()
        self.service = ConversionService(self.clipboard_service, self.converter_registry)
        self.mock_converter = MockConverter("Test", "text/html")

    def test_get_available_converters(self):
        """Test getting available converters."""
        self.clipboard_service.get_available_mimetypes.return_value = ["text/html"]
        self.converter_registry.get_converters_for_mimetypes.return_value = [self.mock_converter]

        converters = self.service.get_available_converters()

        self.assertEqual(len(converters), 1)
        self.assertEqual(converters[0], self.mock_converter)
        self.clipboard_service.get_available_mimetypes.assert_called_once()

    def test_get_clipboard_mimetypes(self):
        """Test getting clipboard MIME types."""
        expected_mimetypes = ["text/html", "text/plain"]
        self.clipboard_service.get_available_mimetypes.return_value = expected_mimetypes

        mimetypes = self.service.get_clipboard_mimetypes()

        self.assertEqual(mimetypes, expected_mimetypes)

    def test_convert_success(self):
        """Test successful conversion."""
        self.clipboard_service.get_content.return_value = "Test content"

        result = self.service.convert(self.mock_converter)

        self.assertEqual(result, "# Test content")
        self.clipboard_service.get_content.assert_called_once_with("text/html")

    def test_convert_no_content(self):
        """Test conversion when clipboard has no content for the mimetype."""
        self.clipboard_service.get_content.return_value = None

        result = self.service.convert(self.mock_converter)

        self.assertIsNone(result)

    def test_convert_and_copy_to_clipboard_success(self):
        """Test converting and copying to clipboard."""
        self.clipboard_service.get_content.return_value = "Test content"

        result = self.service.convert_and_copy_to_clipboard(self.mock_converter)

        self.assertEqual(result, "# Test content")
        self.clipboard_service.set_text.assert_called_once_with("# Test content")

    def test_convert_and_copy_to_clipboard_failure(self):
        """Test converting and copying when conversion fails."""
        self.clipboard_service.get_content.return_value = None

        result = self.service.convert_and_copy_to_clipboard(self.mock_converter)

        self.assertIsNone(result)
        self.clipboard_service.set_text.assert_not_called()

    def test_copy_to_clipboard(self):
        """Test copying edited result text to the clipboard."""
        self.service.copy_to_clipboard("# Edited content")

        self.clipboard_service.set_text.assert_called_once_with("# Edited content")


if __name__ == "__main__":
    unittest.main()

