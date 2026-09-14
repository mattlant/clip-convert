"""Utilities for detecting and updating simple Markdown tables."""
import re
from typing import Optional


class MarkdownTableService:
    """Detect headerless standalone Markdown tables and add their header row."""

    _SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")

    def is_headerless_table(self, markdown: str) -> bool:
        """Return whether markdown contains only a multi-row table without separators."""
        lines = [line for line in markdown.splitlines() if line.strip()]

        if len(lines) < 2:
            return False

        rows = [self._get_cells(line) for line in lines]
        if any(row is None for row in rows):
            return False

        row_lengths = {len(row) for row in rows if row is not None}
        if len(row_lengths) != 1:
            return False

        return not any(self._is_separator_row(row) for row in rows if row is not None)

    def add_header_separator(self, markdown: str) -> str:
        """Insert a Markdown header separator after the first table row."""
        lines = markdown.splitlines(keepends=True)
        first_row_index = next(
            index for index, line in enumerate(lines) if line.strip()
        )
        first_row = self._get_cells(lines[first_row_index])
        assert first_row is not None

        separator = "| " + " | ".join("---" for _ in first_row) + " |\n"
        lines.insert(first_row_index + 1, separator)
        return "".join(lines)

    @classmethod
    def _get_cells(cls, line: str) -> Optional[list[str]]:
        stripped = line.strip()
        if "|" not in stripped:
            return None

        if stripped.startswith("|"):
            stripped = stripped[1:]
        if stripped.endswith("|"):
            stripped = stripped[:-1]

        cells = [cell.strip() for cell in stripped.split("|")]
        return cells if len(cells) >= 2 else None

    @classmethod
    def _is_separator_row(cls, cells: list[str]) -> bool:
        return all(cls._SEPARATOR_CELL.fullmatch(cell) for cell in cells)
