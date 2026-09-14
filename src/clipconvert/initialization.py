"""
Initialization module for registering converters.
"""
from clipconvert.converter_registry import ConverterRegistry
from clipconvert.html_converter import HTMLToMarkdownConverter


def initialize_converters() -> ConverterRegistry:
    """
    Initialize and register all converters.
    Returns:
        ConverterRegistry: Registry with all converters registered
    """
    registry = ConverterRegistry()

    registry.register(HTMLToMarkdownConverter())

    # Add more converters here as they are created
    # Example:
    # excel_converter = ExcelToMarkdownConverter()
    # registry.register(excel_converter)

    return registry

