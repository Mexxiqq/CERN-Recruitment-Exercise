import os
from PyQt6.QtCore import QThread, pyqtSignal
import requests

from .data import fetch_countries
from .config import FLAG_BASE_URL, FLAG_FOLDER


class CountryFetchThread(QThread):
    """
    Thread to fetch the list of countries from the network API.
    Runs fetch_countries() and emits signals on success or failure.
    """
    finished = pyqtSignal(list)  # emits list of (country_name, alpha2_code) tuples
    error = pyqtSignal(str)      # emits error message string

    def run(self) -> None:
        try:
            countries = fetch_countries()
            self.finished.emit(countries)
        except Exception as e:
            self.error.emit(str(e))


class FlagFetchThread(QThread):
    """
    Thread to fetch the flag image (SVG) of a selected country by its alpha2 code.
    Saves the flag locally and emits the local path once done.
    """
    finished = pyqtSignal(str)  # emits local path to saved flag file, or empty string if failed

    def __init__(self, alpha2_code: str):
        super().__init__()
        self.alpha2_code = alpha2_code.lower()

    def run(self) -> None:
        try:
            # Ensure the flag folder exists
            if not os.path.exists(FLAG_FOLDER):
                os.makedirs(FLAG_FOLDER, exist_ok=True)

            filename = f"{self.alpha2_code}.svg"
            local_path = os.path.join(FLAG_FOLDER, filename)

            # Download flag only if not already cached
            if not os.path.isfile(local_path):
                url = f"{FLAG_BASE_URL}/{self.alpha2_code}.svg"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(response.content)

            self.finished.emit(local_path)
        except Exception:
            # On failure, emit empty string to indicate no flag available
            self.finished.emit("")
