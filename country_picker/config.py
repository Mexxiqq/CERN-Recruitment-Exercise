"""
Configuration constants for the Country Picker application.
Adjust these values to customize behavior or API endpoints.
"""

# URL to fetch country data (returns JSON)
API_URL = "https://restcountries.com/v2/all?fields=name,alpha2Code"

# Base URL to download SVG flags
FLAG_BASE_URL = "https://flagcdn.com"
# FLAG_BASE_URL = "https://github.com/lipis/flag-icon-css/raw/main/flags/4x3"

# Folder where downloaded flag files will be stored
FLAG_FOLDER = "flags"

# Logging output directory and file
LOGS_DIR = "logs"
LOG_FILE = f"{LOGS_DIR}/app.log"

# UI label texts
INITIAL_LABEL_PLACEHOLDER = "Selected: <insert country name here>"
COMBOBOX_LOADING_TEXT = "Loading countries..."
COMBOBOX_SELECT_TEXT = "Select a country"
COMBOBOX_NO_COUNTRIES_TEXT = "No countries available"
COMBOBOX_ERROR_TEXT = "Error loading countries"

# Number of seconds to wait before retrying failed country fetch
RETRY_INTERVAL_SECONDS = 5

# MessageBox text when a preselected country isn't found
MESSAGE_BOX_PRESELECT_NOT_FOUND = (
    "The country '{}' was not found in the loaded list."
)
