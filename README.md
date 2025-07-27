# Country Picker

## Overview

Country Picker is a Python desktop application built with PyQt6 that allows users to select a country from a dropdown list and view its flag. The country list is fetched from a remote API, and flag images are downloaded on demand. The UI will run immediately, while the information will be threaded in the background. 
Automatically retries fetching countries if there’s no internet connection, showing a countdown. If the flags aren't retrievable, the UI will display only the countryname, without a flag.

## Features

* Fetches country list dynamically from a REST API: "https://restcountries.com/v2/all?fields=name,alpha2Code"
* Fetches country flag upon selection from: "https://github.com/lipis/flag-icon-css/raw/main/flags/4x3"
* Displays country flags alongside the selected country.
* Supports pre-selecting a country via command line argument.
* Automatically retries fetching countries if there’s no internet connection, showing a countdown. 
* If flags can't be fetched, the UI will only display the countryname, without the flag.
* Threaded network requests to keep UI responsive.

## Requirements

* Python 3.10+
* PyQt6
* requests

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Mexxiqq/CERN-Recruitment-Exercise.git
   cd RecruitmentExercise
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the app:

```bash
python -m country_picker
```

Pre-select a country by name (case-insensitive):

```bash
python -m country_picker --select Switzerland
```

## Testing

Run unit tests with:

```bash
python -m unittest  tests.test_data
```

Test output is logged in `tests/test_data.log`.

## Project Structure

```
RecruitmentExercise/
├── country_picker/           # Main package
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── app.py                # Main application logic and threading
│   ├── ui.py                 # PyQt6 UI components
│   ├── thread.py             # Worker threads for network calls, fetching data
│   ├── utils.py              # Helper functions
│   ├── data.py               # API data fetching
│   ├── config.py             # Configuration constants
│   ├── assets/               # Content loaded dynamically at runtime.
│   │   └── flags/            # (empty, created at runtime, keeps downloaded SVGs here)
│   └── resources/            # Logic of the app, part of compiling the app
│       └── icon.ico/         # app icon, part of the app logic
├── logs/
│   └── app.log               
├── tests/                    
│   ├── __init__.py
│   └── test_data.py          # Unit tests with logging
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # This file

```

## Configuration

Modify constants in `config.py` to change API URLs, retry intervals, log locations, etc.

## License

MIT License

