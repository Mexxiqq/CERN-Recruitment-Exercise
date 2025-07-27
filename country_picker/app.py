import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

from .ui import CountryPickerUI
from .thread import CountryFetchThread, FlagFetchThread
from .config import (
    LOGS_DIR,
    LOG_FILE,
    RETRY_INTERVAL_SECONDS,
    MESSAGE_BOX_PRESELECT_NOT_FOUND,
)

import logging

# Ensure logs directory exists
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class CountryPickerApp:
    """
    Main application controller class.
    Handles UI initialization, threading, and retry logic.
    """

    def __init__(self, preselect: str | None = None):
        """
        Initialize the application and start fetching countries.

        Args:
            preselect: Optional country name to pre-select on startup.
        """
        self.app = QApplication(sys.argv)
        self.ui = CountryPickerUI()
        self.ui.show()

        self.preselect = preselect
        self.countries: list[tuple[str, str]] = []
        self.flag_fetch_thread: FlagFetchThread | None = None

        # Retry timer for re-fetching countries after errors
        self.retry_timer = QTimer()
        self.retry_timer.setInterval(1000)  # Tick every 1 second
        self.seconds_remaining = RETRY_INTERVAL_SECONDS

        # Start initial fetch thread
        self.fetch_thread = CountryFetchThread()
        self.fetch_thread.finished.connect(self.on_countries_fetched)
        self.fetch_thread.error.connect(self.on_fetch_error)
        self.fetch_thread.start()

        # Connect UI events
        self.ui.combobox.currentIndexChanged.connect(self.on_country_selected)
        self.retry_timer.timeout.connect(self.update_retry_countdown)

    def on_countries_fetched(self, countries: list[tuple[str, str]]) -> None:
        """
        Handle successful country fetch.

        Args:
            countries: List of (country_name, alpha2_code) tuples.
        """
        self.retry_timer.stop()
        self.ui.update_retry_label(None)
        self.countries = sorted(countries, key=lambda x: x[0])
        self.ui.set_countries(self.countries)

        # If preselect specified, set it in combobox or warn if not found
        if self.preselect:
            index = next(
                (i + 1 for i, (name, _) in enumerate(self.countries) if name.lower() == self.preselect.lower()),
                None,
            )
            if index is not None:
                self.ui.combobox.setCurrentIndex(index)
            else:
                QMessageBox.warning(
                    self.ui,
                    "Preselect not found",
                    MESSAGE_BOX_PRESELECT_NOT_FOUND.format(self.preselect),
                )

    def on_fetch_error(self, error_msg: str) -> None:
        """
        Handle errors in fetching countries.

        Args:
            error_msg: Error message string.
        """
        logging.error(f"Error fetching countries: {error_msg}")
        self.ui.show_error_loading()
        self.seconds_remaining = RETRY_INTERVAL_SECONDS
        self.retry_timer.start()
        self.ui.update_retry_label(self.seconds_remaining)

    def update_retry_countdown(self) -> None:
        """
        Countdown timer handler for retrying country fetch.
        """
        self.seconds_remaining -= 1
        if self.seconds_remaining <= 0:
            # Time to retry fetching countries
            self.retry_timer.stop()
            self.ui.update_retry_label(None)

            self.fetch_thread = CountryFetchThread()
            self.fetch_thread.finished.connect(self.on_countries_fetched)
            self.fetch_thread.error.connect(self.on_fetch_error)
            self.fetch_thread.start()
        else:
            self.ui.update_retry_label(self.seconds_remaining)

    def on_country_selected(self, index: int) -> None:
        """
        Handle user selecting a country from the combobox.

        Args:
            index: The selected index of the combobox.
        """
        if index <= 0 or index - 1 >= len(self.countries):
            # No valid selection
            self.ui.update_label("", None)
            return

        country_name, alpha2 = self.countries[index - 1]
        # Show country name immediately without flag
        self.ui.update_label(country_name, None)

        # Stop previous flag fetch thread if running
        if self.flag_fetch_thread is not None:
            self.flag_fetch_thread.quit()
            self.flag_fetch_thread.wait()

        # Start new thread to fetch flag icon asynchronously
        self.flag_fetch_thread = FlagFetchThread(alpha2)
        self.flag_fetch_thread.finished.connect(
            lambda path: self.ui.update_label(country_name, path)
        )
        self.flag_fetch_thread.start()

    def run(self) -> None:
        """
        Start the Qt application event loop.
        """
        sys.exit(self.app.exec())
