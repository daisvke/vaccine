import argparse
from urllib.parse import parse_qs, urlparse

from utils.constants import SYSTEM_DATABASES


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    # Target URL
    p.add_argument("url", type=str, help="Target URL")

    # Method used by the request
    p.add_argument(
        "-X",
        "--method",
        type=str,
        default="GET",
        choices=["GET", "POST", "PATCH", "PUT", "DELETE"],
        help="HTTP method",
    )

    # Results storage file name
    p.add_argument(
        "-o", "--output", type=str, default="vaccine.json", help="Output file"
    )

    # Enable debug mode
    p.add_argument("-D", "--debug", action="store_true", help="Enable debug mode")

    # Use custom User-Agent
    p.add_argument("-A", "--agent", type=str, help="Custom User-Agent")

    return p.parse_args()


def extract_params(url: str) -> dict[str, str]:
    """
    Extract parameters and their first value from a URL.

    Example:
    https://example.com?page=1&user=admin
    -> {"page": "1", "user": "admin"}
    """
    query = urlparse(url).query

    parsed = parse_qs(query)

    return {param: values[0] for param, values in parsed.items()}


def is_system_db(database_name: str) -> bool:
    return database_name.lower() in SYSTEM_DATABASES
