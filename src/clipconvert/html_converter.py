"""
HTML to Markdown converter using markdownify library.
This converter implements the same BaseConverter interface but delegates
conversion to the markdownify.markdownify function which produces
standard Markdown from HTML.

The converter post-processes markdownify output to match the existing
conventions used by the original converter (dash list markers and
`1.` numbering for ordered lists used consistently).
"""
from clipconvert.base_converter import BaseConverter
from typing import Optional
import re

try:
    from markdownify import markdownify as mdify
except Exception as e:
    mdify = None


class HTMLToMarkdownConverter(BaseConverter):
    """HTML to Markdown converter using markdownify."""

    @property
    def display_text(self) -> str:
        return "HTML to Markdown"

    @property
    def supported_mimetype(self) -> str:
        return "text/html"

    def convert(self, content: str) -> str:
        """
        Convert HTML content to Markdown using markdownify.
        If markdownify is not available, raise an informative ImportError.

        Post-process the markdownify output to match the formatting expectations
        of the rest of the application/tests:
          - Use '-' for unordered list markers (not '*' or '+')
          - Normalize ordered list numbering to use '1.' for every item
        """
        if mdify is None:
            raise ImportError("markdownify is not installed. Please install requirements.txt.")

        # Produce initial markdown using markdownify
        md = mdify(content, heading_style="ATX")

        # Replace unordered list markers (*, +) with '-'
        # Preserve indentation
        md = re.sub(r'(?m)^(\s*)[*+]\s+', r"\1- ", md)

        # Normalize ordered list numbering to '1.' for each item
        md = re.sub(r'(?m)^(\s*)\d+\.\s+', r"\g<1>1. ", md)

        # Some markdownify outputs use '+' for nested lists; ensure those are converted
        md = re.sub(r'(?m)^(\s*)\+\s+', r"\1- ", md)

        # Collapse excessive trailing whitespace on lines
        md = re.sub(r'[ \t]+\n', '\n', md)

        return md
