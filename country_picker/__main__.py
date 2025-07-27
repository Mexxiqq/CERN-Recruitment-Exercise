"""
Entrypoint for the country_picker package.
Parses command-line arguments and launches the Country Picker application.
"""

import argparse
from .app import CountryPickerApp


def main() -> None:
    """
    Parses optional CLI arguments and starts the Qt application.
    """
    parser = argparse.ArgumentParser(description="Country Picker")
    parser.add_argument(
        "--select",
        type=str,
        help="Pre-select a country name in the dropdown",
        default=None,
    )
    args = parser.parse_args()

    # Initialize the application with optional preselected country
    app = CountryPickerApp(preselect=args.select)
    exit_code = app.run()
    exit(exit_code)


if __name__ == "__main__":
    main()
