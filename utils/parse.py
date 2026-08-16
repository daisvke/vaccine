import argparse
from urllib.parse import parse_qs, urlparse

from utils.constants import SYSTEM_DATABASES


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    # Target URL
    p.add_argument(
        "url",
        type=str,
        nargs="?",
        help="Target URL with its parameters."
        "All methods need its data given in the form of valid parameters and values."
        "Example: http://localhost:8080/user.php?id=1",
    )

    # Results viewer mode
    p.add_argument("-V", "--view", type=int, help="View the formatted results with the given result ID")

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

    args = p.parse_args()

    if args.url is None and args.view is None:
        p.error("a URL or --view must be provided")

    if args.url is not None and args.view is not None:
        p.error("URL and --view cannot be used together")

    return args


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
