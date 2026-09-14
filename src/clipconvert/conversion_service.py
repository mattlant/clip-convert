"""
Conversion service for managing the conversion process.
"""
from typing import Optional, List
from clipconvert.base_converter import BaseConverter
from clipconvert.clipboard_service import ClipboardService
from clipconvert.converter_registry import ConverterRegistry


class ConversionService:
    """Service that orchestrates the conversion process."""

    def __init__(self, clipboard_service: ClipboardService,
                 converter_registry: ConverterRegistry):
        self._clipboard_service = clipboard_service
        self._converter_registry = converter_registry

    def get_available_converters(self) -> List[BaseConverter]:
        """
        Get all converters that can handle current clipboard content.
        Returns:
            List of available converters
        """
        mimetypes = self._clipboard_service.get_available_mimetypes()
        return self._converter_registry.get_converters_for_mimetypes(mimetypes)

    def get_clipboard_mimetypes(self) -> List[str]:
        """
        Get all MIME types currently on the clipboard.
        Returns:
            List of MIME type strings
        """
        return self._clipboard_service.get_available_mimetypes()

    def convert(self, converter: BaseConverter) -> Optional[str]:
        """
        Convert clipboard content using the specified converter.
        Args:
            converter: The converter to use
        Returns:
            Markdown content or None if conversion failed
        """
        mimetype = converter.supported_mimetype
        content = self._clipboard_service.get_content(mimetype)

        if content is None:
            return None

        return converter.convert(content)

    def convert_and_copy_to_clipboard(self, converter: BaseConverter) -> Optional[str]:
        """
        Convert content and copy result to clipboard.
        Args:
            converter: The converter to use
        Returns:
            Markdown content or None if conversion failed
        """
        markdown = self.convert(converter)

        if markdown is not None:
            self._clipboard_service.set_text(markdown)

        return markdown

    def copy_to_clipboard(self, text: str) -> None:
        """Copy text to the clipboard."""
        self._clipboard_service.set_text(text)
