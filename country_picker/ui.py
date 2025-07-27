import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

from .config import (
    INITIAL_LABEL_PLACEHOLDER,
    COMBOBOX_LOADING_TEXT,
    COMBOBOX_SELECT_TEXT,
    COMBOBOX_NO_COUNTRIES_TEXT,
    COMBOBOX_ERROR_TEXT,
)


class CountryPickerUI(QWidget):
    """
    Main UI Widget containing the combo box, flag label, country name label,
    and a retry countdown label.

    The layout places the combo box at the top and a horizontal layout below it
    with the selected country name and its flag icon.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Country Picker")
        self.setMinimumSize(600, 250)

        # Set custom window icon
        icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        # Main vertical layout for the widget
        self.layout = QVBoxLayout(self)

        # Setup ComboBox with initial loading text
        self.combobox = QComboBox(self)
        combo_font = QFont()
        combo_font.setPointSize(14)
        self.combobox.setFont(combo_font)
        self.combobox.setEditable(False)
        self.combobox.addItem(COMBOBOX_LOADING_TEXT)

        # Horizontal layout to hold flag and selected country text side by side
        flag_text_layout = QHBoxLayout()

        # Label to show the flag icon (scaled)
        self.flag_label = QLabel(self)
        self.flag_label.setFixedSize(48, 32)  # smaller size to roughly match font height
        self.flag_label.setScaledContents(True)
        self.flag_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label to show the selected country name text
        self.text_label = QLabel(INITIAL_LABEL_PLACEHOLDER, self)
        text_font = QFont()
        text_font.setPointSize(16)
        text_font.setBold(True)
        self.text_label.setFont(text_font)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        flag_text_layout.addWidget(self.text_label)
        flag_text_layout.addWidget(self.flag_label)
        flag_text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label to display retry countdown seconds or error messages below
        self.retry_label = QLabel("", self)
        retry_font = QFont()
        retry_font.setPointSize(12)
        retry_font.setItalic(True)
        self.retry_label.setFont(retry_font)
        self.retry_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets/layouts to main layout
        self.layout.addWidget(self.combobox)
        self.layout.addLayout(flag_text_layout)
        self.layout.addWidget(self.retry_label)

    def set_countries(self, countries: list[tuple[str, str]]) -> None:
        """
        Populate the combo box with country names.

        Args:
            countries (list[tuple[str, str]]): List of (country_name, alpha2_code)
        """
        self.combobox.clear()
        if not countries:
            self.combobox.addItem(COMBOBOX_NO_COUNTRIES_TEXT)
            self.combobox.setEnabled(False)
            return

        self.combobox.setEnabled(True)
        self.combobox.addItem(COMBOBOX_SELECT_TEXT)
        for country, _alpha2 in countries:
            self.combobox.addItem(country)

    def show_error_loading(self) -> None:
        """
        Show error message in combo box when loading countries fails.
        """
        self.combobox.clear()
        self.combobox.addItem(COMBOBOX_ERROR_TEXT)
        self.combobox.setEnabled(False)

    def update_label(self, country_name: str, flag_path: str | None) -> None:
        """
        Update the selected country label and display the flag icon.

        Args:
            country_name (str): Name of the selected country.
            flag_path (str | None): Local path to flag image (SVG or other).
        """
        if not country_name:
            self.text_label.setText(INITIAL_LABEL_PLACEHOLDER)
            self.flag_label.clear()
            return

        # Display "Selected: <country_name>"
        self.text_label.setText(f"Selected: {country_name}")

        if flag_path and os.path.exists(flag_path):
            icon = QIcon(flag_path)
            pixmap = icon.pixmap(self.flag_label.width(), self.flag_label.height())
            self.flag_label.setPixmap(pixmap)
        else:
            self.flag_label.clear()

    def update_retry_label(self, seconds_remaining: int | None) -> None:
        """
        Update the retry countdown label shown below the main UI.

        Args:
            seconds_remaining (int | None): Seconds left until next retry.
                If None, clear the retry label.
        """
        if seconds_remaining is None:
            self.retry_label.setText("")
        else:
            self.retry_label.setText(f"Retrying in {seconds_remaining} seconds...")
