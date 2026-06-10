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

	p.add_argument(
		"-d",
		"--debug",
		action='store_true',
		help="Enable debug mode"
	)

	return p.parse_args()

def extract_params(url: str) -> dict[str, list[str]]:
	"""
	Extracts the parameters from a URL.
	Ex.: `page` in `https://example.com?page=1`
	"""
	query = urlparse(url).query
	parsed = parse_qs(query)

	return parsed
