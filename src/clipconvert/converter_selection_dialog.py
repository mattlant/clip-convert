"""
Converter selection dialog for choosing between multiple converters.
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QPushButton,
                                QLabel, QWidget)
from PySide6.QtCore import Qt
from typing import List, Optional
from clipconvert.base_converter import BaseConverter


class ConverterSelectionDialog(QDialog):
    """Modal dialog for selecting a converter."""

    def __init__(self, converters: List[BaseConverter], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._converters = converters
        self._selected_converter: Optional[BaseConverter] = None
        self._setup_ui()

    def _setup_ui(self):
        """Set up the dialog UI."""
        self.setWindowTitle("Select Converter")
        self.setModal(True)

        layout = QVBoxLayout()

        # Add instruction label
        label = QLabel("Multiple converters available. Please select one:")
        layout.addWidget(label)

        # Add a button for each converter
        for converter in self._converters:
            button_text = f"{converter.display_text} ({converter.supported_mimetype})"
            button = QPushButton(button_text)
            button.clicked.connect(lambda checked=False, c=converter: self._on_converter_selected(c))
            layout.addWidget(button)

        self.setLayout(layout)

    def _on_converter_selected(self, converter: BaseConverter):
        """Handle converter selection."""
        self._selected_converter = converter
        self.accept()

    def get_selected_converter(self) -> Optional[BaseConverter]:
        """
        Get the selected converter.
        Returns:
            The selected converter or None if dialog was cancelled
        """
        return self._selected_converter

