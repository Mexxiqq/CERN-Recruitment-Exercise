from typing import List, Tuple
import requests
from .utils import parse_countries_json
from .config import API_URL


def fetch_countries() -> List[Tuple[str, str]]:
    """
    Fetch the list of countries from the API_URL.
    Parses and returns a list of (country_name, alpha2_code) tuples.

    Raises:
        requests.RequestException: For network-related errors.
        ValueError: If response JSON is invalid or cannot be parsed.
    """
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()  # Raise HTTPError for bad responses

    json_data = response.json()
    return parse_countries_json(json_data)
