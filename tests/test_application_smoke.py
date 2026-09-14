"""Application-wide import and converter initialization smoke tests."""
import importlib
import unittest

from clipconvert.initialization import initialize_converters


class TestApplicationSmoke(unittest.TestCase):
    def test_required_application_modules_import(self):
        modules = (
            "clipconvert.config",
            "clipconvert.base_converter",
            "clipconvert.html_converter",
            "clipconvert.converter_registry",
            "clipconvert.clipboard_service",
            "clipconvert.conversion_service",
            "clipconvert.converter_selection_dialog",
            "clipconvert.main_window",
            "clipconvert.initialization",
            "clipconvert.main",
        )

        for module_name in modules:
            with self.subTest(module=module_name):
                self.assertIsNotNone(importlib.import_module(module_name))

    def test_converter_initialization_registers_active_html_converter(self):
        registry = initialize_converters()

        converters = registry.get_converters_for_mimetype("text/html")

        self.assertEqual(len(converters), 1)
        self.assertEqual(converters[0].display_text, "HTML to Markdown")


if __name__ == "__main__":
    unittest.main()
