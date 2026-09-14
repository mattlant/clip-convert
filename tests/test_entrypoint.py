"""Tests for the installed application entrypoint."""
import unittest

from clipconvert.main import main


class TestEntrypoint(unittest.TestCase):
    def test_main_is_callable(self):
        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
