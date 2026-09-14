"""
Converter registry for managing all available converters.
"""
from typing import Dict, List
from clipconvert.base_converter import BaseConverter


class ConverterRegistry:
    """Registry for managing converter instances."""

    def __init__(self):
        self._converters: Dict[str, List[BaseConverter]] = {}

    def register(self, converter: BaseConverter):
        """
        Register a converter.
        Args:
            converter: The converter instance to register
        """
        mimetype = converter.supported_mimetype

        if mimetype not in self._converters:
            self._converters[mimetype] = []

        self._converters[mimetype].append(converter)

    def get_converters_for_mimetype(self, mimetype: str) -> List[BaseConverter]:
        """
        Get all converters that support a given MIME type.
        Args:
            mimetype: The MIME type to search for
        Returns:
            List of converters that support the MIME type
        """
        return self._converters.get(mimetype, [])

    def get_converters_for_mimetypes(self, mimetypes: List[str]) -> List[BaseConverter]:
        """
        Get all converters that support any of the given MIME types.
        Args:
            mimetypes: List of MIME types to search for
        Returns:
            List of converters that support any of the MIME types
        """
        converters = []
        seen = set()

        for mimetype in mimetypes:
            for converter in self.get_converters_for_mimetype(mimetype):
                # Avoid duplicates
                converter_id = id(converter)
                if converter_id not in seen:
                    converters.append(converter)
                    seen.add(converter_id)

        return converters

    def get_all_supported_mimetypes(self) -> List[str]:
        """
        Get all MIME types that have registered converters.
        Returns:
            List of supported MIME types
        """
        return list(self._converters.keys())

