from urllib.parse import urlparse, parse_qs

import argparse


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    p.add_argument(
        "url",
        type=str,
        help="Target URL"
    )

    p.add_argument(
        "-X",
        "--method",
        type=str,
        default="GET",
        choices=["GET", "POST"],
        help="HTTP method"
    )

    p.add_argument(
        "-o",
        "--output",
        type=str,
        default="vaccine.json",
        help="Output file"
    )

    return p.parse_args()

def extract_params(url: str) -> dict[str, list[str]]:
    query = urlparse(url).query
    parsed = parse_qs(query)

    return parsed
