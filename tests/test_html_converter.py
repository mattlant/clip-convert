"""
Unit tests for the markdownify-based HTML to Markdown converter.
"""
import unittest
from clipconvert.html_converter import HTMLToMarkdownConverter


class TestHTMLToMarkdownConverter(unittest.TestCase):
    """Test cases for HTMLToMarkdownConverter."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = HTMLToMarkdownConverter()

    def test_display_text(self):
        """Test display text property."""
        self.assertEqual(self.converter.display_text, "HTML to Markdown")

    def test_supported_mimetype(self):
        """Test supported mimetype property."""
        self.assertEqual(self.converter.supported_mimetype, "text/html")

    def test_convert_plain_text(self):
        """Test converting plain text."""
        html = "Hello World"
        result = self.converter.convert(html)
        self.assertEqual(result.strip(), "Hello World")

    def test_convert_paragraph(self):
        """Test converting paragraph."""
        html = "<p>This is a paragraph.</p>"
        result = self.converter.convert(html)
        self.assertIn("This is a paragraph.", result)

    def test_convert_headings(self):
        """Test converting headings."""
        test_cases = [
            ("<h1>Heading 1</h1>", "# Heading 1"),
            ("<h2>Heading 2</h2>", "## Heading 2"),
            ("<h3>Heading 3</h3>", "### Heading 3"),
            ("<h4>Heading 4</h4>", "#### Heading 4"),
            ("<h5>Heading 5</h5>", "##### Heading 5"),
            ("<h6>Heading 6</h6>", "###### Heading 6"),
        ]

        for html, expected in test_cases:
            result = self.converter.convert(html)
            self.assertIn(expected, result)

    def test_convert_bold(self):
        """Test converting bold text."""
        html = "<strong>Bold text</strong>"
        result = self.converter.convert(html)
        self.assertIn("**Bold text**", result)

        html = "<b>Bold text</b>"
        result = self.converter.convert(html)
        self.assertIn("**Bold text**", result)

    def test_convert_italic(self):
        """Test converting italic text."""
        html = "<em>Italic text</em>"
        result = self.converter.convert(html)
        self.assertIn("*Italic text*", result)

        html = "<i>Italic text</i>"
        result = self.converter.convert(html)
        self.assertIn("*Italic text*", result)

    def test_convert_link(self):
        """Test converting links."""
        html = '<a href="https://example.com">Example Link</a>'
        result = self.converter.convert(html)
        self.assertIn("[Example Link](https://example.com)", result)

    def test_convert_image(self):
        """Test converting images."""
        html = '<img src="image.jpg" alt="An image">'
        result = self.converter.convert(html)
        self.assertIn("![An image](image.jpg)", result)

    def test_convert_unordered_list(self):
        """Test converting unordered lists."""
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        result = self.converter.convert(html)
        self.assertIn("- Item 1", result)
        self.assertIn("- Item 2", result)

    def test_convert_ordered_list(self):
        """Test converting ordered lists."""
        html = "<ol><li>First</li><li>Second</li></ol>"
        result = self.converter.convert(html)
        self.assertIn("1. First", result)
        self.assertIn("1. Second", result)

    def test_convert_code_inline(self):
        """Test converting inline code."""
        html = "<code>inline code</code>"
        result = self.converter.convert(html)
        self.assertIn("`inline code`", result)

    def test_convert_code_block(self):
        """Test converting code blocks."""
        html = "<pre><code>code block</code></pre>"
        result = self.converter.convert(html)
        self.assertIn("```", result)
        self.assertIn("code block", result)

    def test_convert_blockquote(self):
        """Test converting blockquotes."""
        html = "<blockquote>This is a quote</blockquote>"
        result = self.converter.convert(html)
        self.assertIn("> This is a quote", result)

    def test_convert_horizontal_rule(self):
        """Test converting horizontal rules."""
        html = "<hr>"
        result = self.converter.convert(html)
        self.assertIn("---", result)

    def test_convert_line_break(self):
        """Test converting line breaks."""
        html = "Line 1<br>Line 2"
        result = self.converter.convert(html)
        self.assertIn("Line 1", result)
        self.assertIn("Line 2", result)

    def test_convert_complex_html(self):
        """Test converting complex HTML with multiple elements."""
        html = """
        <h1>Title</h1>
        <p>This is a <strong>paragraph</strong> with <em>formatting</em>.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        <p>Visit <a href="https://example.com">this link</a>.</p>
        """
        result = self.converter.convert(html)

        self.assertIn("# Title", result)
        self.assertIn("**paragraph**", result)
        self.assertIn("*formatting*", result)
        self.assertIn("- Item 1", result)
        self.assertIn("- Item 2", result)
        self.assertIn("[this link](https://example.com)", result)

    def test_convert_nested_lists(self):
        """Test converting nested lists."""
        html = """
        <ul>
            <li>Item 1
                <ul>
                    <li>Subitem 1</li>
                    <li>Subitem 2</li>
                </ul>
            </li>
            <li>Item 2</li>
        </ul>
        """
        result = self.converter.convert(html)
        self.assertIn("- Item 1", result)
        self.assertIn("- Subitem 1", result)
        self.assertIn("- Item 2", result)

    def test_whitespace_normalization(self):
        """Test that whitespace is properly normalized."""
        html = "<p>Text   with   multiple   spaces</p>"
        result = self.converter.convert(html)
        self.assertIn("Text with multiple spaces", result)


if __name__ == "__main__":
    unittest.main()

