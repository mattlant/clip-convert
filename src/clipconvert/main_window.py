"""
Main window for ClipConvert application.
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QLabel,
                                QTextEdit, QMessageBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from clipconvert.conversion_service import ConversionService
from clipconvert.converter_selection_dialog import ConverterSelectionDialog
from clipconvert.markdown_table_service import MarkdownTableService
from clipconvert import config


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, conversion_service: ConversionService):
        super().__init__()
        self._conversion_service = conversion_service
        self._markdown_table_service = MarkdownTableService()
        self._setup_ui()

    def _setup_ui(self):
        """Set up the main window UI."""
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.setWindowIcon(QIcon(str(config.ICON_PATH)))

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create top layout with label and button
        top_layout = QHBoxLayout()

        # Add label
        label = QLabel("Convert clipboard content to Markdown:")
        top_layout.addWidget(label)

        # Add convert button
        self._convert_button = QPushButton("Convert && Copy")
        self._convert_button.clicked.connect(self._on_convert_clicked)
        top_layout.addWidget(self._convert_button)

        self._copy_button = QPushButton("Copy")
        self._copy_button.clicked.connect(self._on_copy_clicked)
        top_layout.addWidget(self._copy_button)

        main_layout.addLayout(top_layout)

        # Add results text box
        self._results_text = QTextEdit()
        self._results_text.setPlaceholderText("Conversion results will appear here...")
        main_layout.addWidget(self._results_text)

        self._version_label = QLabel(f"{config.APP_NAME} {config.APP_VERSION}")
        self._version_label.setFocusPolicy(Qt.NoFocus)
        self._version_label.setStyleSheet("color: #888888;")
        main_layout.addWidget(self._version_label)

        # Apply dark theme if configured
        if config.THEME == "dark":
            self._apply_dark_theme()

    def _apply_dark_theme(self):
        """Apply dark theme to the application."""
        dark_stylesheet = """
            QMainWindow, QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                padding: 5px;
            }
            QPushButton {
                background-color: #0e639c;
                color: #ffffff;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #0d5a8f;
            }
            QLabel {
                color: #cccccc;
            }
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def _on_convert_clicked(self):
        """Handle convert button click."""
        converters = self._conversion_service.get_available_converters()

        # Check if any converters are available
        if not converters:
            self._show_no_converters_error()
            return

        # Determine which converter to use
        selected_converter = None

        if len(converters) == 1:
            # Only one converter available, use it
            selected_converter = converters[0]
        else:
            # Multiple converters available, show selection dialog
            dialog = ConverterSelectionDialog(converters, self)
            if dialog.exec():
                selected_converter = dialog.get_selected_converter()

        # If a converter was selected, perform conversion
        if selected_converter:
            markdown = self._conversion_service.convert(selected_converter)
            if markdown is not None:
                self._results_text.setPlainText(markdown)
                if self._markdown_table_service.is_headerless_table(markdown):
                    answer = QMessageBox.question(
                        self,
                        "Table detected",
                        "Table detected. Use first row as headers?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    )
                    if answer == QMessageBox.StandardButton.Yes:
                        markdown = self._markdown_table_service.add_header_separator(markdown)
                        self._results_text.setPlainText(markdown)

                self._conversion_service.copy_to_clipboard(markdown)
            else:
                self._results_text.setPlainText("Error: Failed to convert clipboard content.")

    def _on_copy_clicked(self):
        """Copy the current result text to the clipboard."""
        self._conversion_service.copy_to_clipboard(self._results_text.toPlainText())

    def _show_no_converters_error(self):
        """Display error message when no converters are available."""
        mimetypes = self._conversion_service.get_clipboard_mimetypes()

        error_message = "Error: No converters available for clipboard content.\n\n"
        error_message += "Available MIME types on clipboard:\n"

        if mimetypes:
            for mimetype in mimetypes:
                error_message += f"  - {mimetype}\n"
        else:
            error_message += "  (clipboard is empty)\n"

        self._results_text.setPlainText(error_message)
