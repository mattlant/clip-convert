"""Unit tests for Markdown table post-processing."""
import unittest

from clipconvert.markdown_table_service import MarkdownTableService


class TestMarkdownTableService(unittest.TestCase):
    def setUp(self):
        self.service = MarkdownTableService()

    def test_detects_headerless_standalone_table(self):
        markdown = "| Name | Value |\n| A | 1 |\n"

        self.assertTrue(self.service.is_headerless_table(markdown))

    def test_rejects_existing_separator(self):
        markdown = "| Name | Value |\n| --- | --- |\n| A | 1 |\n"

        self.assertFalse(self.service.is_headerless_table(markdown))

    def test_rejects_mixed_content(self):
        markdown = "# Data\n\n| Name | Value |\n| A | 1 |\n"

        self.assertFalse(self.service.is_headerless_table(markdown))

    def test_requires_at_least_two_rows(self):
        self.assertFalse(self.service.is_headerless_table("| Name | Value |\n"))

    def test_adds_separator_after_first_row(self):
        markdown = "| Name | Value |\n| A | 1 |\n"

        result = self.service.add_header_separator(markdown)

        self.assertEqual(
            result,
            "| Name | Value |\n| --- | --- |\n| A | 1 |\n",
        )


if __name__ == "__main__":
    unittest.main()
