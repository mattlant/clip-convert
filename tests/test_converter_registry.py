"""
Unit tests for converter registry.
"""
import unittest
from clipconvert.converter_registry import ConverterRegistry
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
        return f"Converted: {content}"


class TestConverterRegistry(unittest.TestCase):
    """Test cases for ConverterRegistry."""

    def setUp(self):
        """Set up test fixtures."""
        self.registry = ConverterRegistry()
        self.html_converter = MockConverter("HTML", "text/html")
        self.plain_converter = MockConverter("Plain Text", "text/plain")
        self.another_html_converter = MockConverter("HTML Alt", "text/html")

    def test_register_single_converter(self):
        """Test registering a single converter."""
        self.registry.register(self.html_converter)
        converters = self.registry.get_converters_for_mimetype("text/html")
        self.assertEqual(len(converters), 1)
        self.assertEqual(converters[0], self.html_converter)

    def test_register_multiple_converters_same_mimetype(self):
        """Test registering multiple converters for the same MIME type."""
        self.registry.register(self.html_converter)
        self.registry.register(self.another_html_converter)

        converters = self.registry.get_converters_for_mimetype("text/html")
        self.assertEqual(len(converters), 2)
        self.assertIn(self.html_converter, converters)
        self.assertIn(self.another_html_converter, converters)

    def test_register_multiple_converters_different_mimetypes(self):
        """Test registering converters for different MIME types."""
        self.registry.register(self.html_converter)
        self.registry.register(self.plain_converter)

        html_converters = self.registry.get_converters_for_mimetype("text/html")
        plain_converters = self.registry.get_converters_for_mimetype("text/plain")

        self.assertEqual(len(html_converters), 1)
        self.assertEqual(len(plain_converters), 1)
        self.assertEqual(html_converters[0], self.html_converter)
        self.assertEqual(plain_converters[0], self.plain_converter)

    def test_get_converters_for_nonexistent_mimetype(self):
        """Test getting converters for a MIME type with no converters."""
        converters = self.registry.get_converters_for_mimetype("application/json")
        self.assertEqual(len(converters), 0)

    def test_get_converters_for_mimetypes(self):
        """Test getting converters for multiple MIME types."""
        self.registry.register(self.html_converter)
        self.registry.register(self.plain_converter)

        converters = self.registry.get_converters_for_mimetypes(["text/html", "text/plain"])
        self.assertEqual(len(converters), 2)
        self.assertIn(self.html_converter, converters)
        self.assertIn(self.plain_converter, converters)

    def test_get_converters_for_mimetypes_no_duplicates(self):
        """Test that get_converters_for_mimetypes doesn't return duplicates."""
        self.registry.register(self.html_converter)

        # Request same mimetype twice
        converters = self.registry.get_converters_for_mimetypes(["text/html", "text/html"])
        self.assertEqual(len(converters), 1)

    def test_get_all_supported_mimetypes(self):
        """Test getting all supported MIME types."""
        self.registry.register(self.html_converter)
        self.registry.register(self.plain_converter)

        mimetypes = self.registry.get_all_supported_mimetypes()
        self.assertEqual(len(mimetypes), 2)
        self.assertIn("text/html", mimetypes)
        self.assertIn("text/plain", mimetypes)


if __name__ == "__main__":
    unittest.main()

