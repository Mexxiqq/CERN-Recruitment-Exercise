from typing import List, Dict, Tuple


def parse_countries_json(json_data: List[Dict]) -> List[Tuple[str, str]]:
    """
    Parse the JSON response from the countries API into a sorted list of tuples.

    Each tuple contains:
        - country name (str)
        - alpha2 country code (str, lowercase)

    Args:
        json_data (List[Dict]): Raw JSON list of country data.

    Returns:
        List[Tuple[str, str]]: List of (country_name, alpha2_code) sorted alphabetically by country name.
    """
    countries = []
    for item in json_data:
        name = item.get("name")
        # Support both 'alpha2Code' and 'alpha2' keys for alpha2 code
        alpha2 = item.get("alpha2Code") or item.get("alpha2")

        if name and alpha2:
            countries.append((name, alpha2.lower()))

    # Sort countries alphabetically by name
    countries.sort(key=lambda x: x[0])
    return countries
