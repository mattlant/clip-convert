"""
Base converter interface for ClipConvert application.
All converters must inherit from this base class.
"""
from abc import ABC, abstractmethod


class BaseConverter(ABC):
    """Abstract base class for all converters."""

    @property
    @abstractmethod
    def display_text(self) -> str:
        """
        Display text to show in the UI.
        Returns:
            str: User-friendly name for the converter
        """
        pass

    @property
    @abstractmethod
    def supported_mimetype(self) -> str:
        """
        The MIME type this converter supports.
        Returns:
            str: MIME type string (e.g., 'text/html')
        """
        pass

    @abstractmethod
    def convert(self, content: str) -> str:
        """
        Convert the input content to markdown.
        Args:
            content: The content to convert
        Returns:
            str: Markdown formatted content
        """
        pass

