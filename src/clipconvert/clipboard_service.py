"""
Clipboard service for handling clipboard operations.
"""
from typing import List, Optional
from PySide6.QtGui import QClipboard


class ClipboardService:
    """Service for interacting with the system clipboard."""

    def __init__(self, clipboard: QClipboard):
        self._clipboard = clipboard

    def get_available_mimetypes(self) -> List[str]:
        """
        Get all available MIME types on the clipboard.
        Returns:
            List of MIME type strings
        """
        mime_data = self._clipboard.mimeData()
        if not mime_data:
            return []

        return mime_data.formats()

    def get_content(self, mimetype: str) -> Optional[str]:
        """
        Get clipboard content for a specific MIME type.
        Args:
            mimetype: The MIME type to retrieve
        Returns:
            Content as string or None if not available
        """
        mime_data = self._clipboard.mimeData()
        if not mime_data or not mime_data.hasFormat(mimetype):
            return None

        data = mime_data.data(mimetype)
        if data:
            # Try to decode as UTF-8, fallback to latin-1
            try:
                return data.data().decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return data.data().decode('latin-1')
                except UnicodeDecodeError:
                    return None

        return None

    def set_text(self, text: str):
        """
        Set plain text on the clipboard.
        Args:
            text: The text to set
        """
        self._clipboard.setText(text)

