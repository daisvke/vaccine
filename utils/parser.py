from urllib.parse import urlparse, parse_qs
import argparse
from utils.logger import Logger


def parse_args() -> argparse.Namespace:
	p = argparse.ArgumentParser()

	# Target URL
	p.add_argument(
		"url",
		type=str,
		help="Target URL"
	)

	# Method used by the request
	p.add_argument(
		"-X",
		"--method",
		type=str,
		default="GET",
		choices=["GET", "POST"],
		help="HTTP method"
	)

	# Results storage file name
	p.add_argument(
		"-o",
		"--output",
		type=str,
		default="vaccine.json",
		help="Output file"
	)

	# Enable debug mode
	p.add_argument(
		"-D",
		"--debug",
		action='store_true',
		help="Enable debug mode"
	)

	# Use custom User-Agent
	p.add_argument(
		"-A",
		"--agent",
		type=str,
		help="Custom User-Agent"
	)

	# Login before injection
	p.add_argument(
		"-L",
		"--login-url",
		type=str,
		help="Login URL"
	)

	# Login username
	p.add_argument(
		"-u",
		"--username",
		type=str,
		help="Login username"
	)

	# Login password
	p.add_argument(
		"-p",
		"--password",
		type=str,
		help="Login password"
	)

	return p.parse_args()

def extract_params(url: str) -> dict[str, list[str]]:
	"""
	Extracts the parameters from a URL.
	Ex.: `page` in `https://example.com?page=1`
	"""
	query = urlparse(url).query
	Logger.debug(f"------- query: {query}")
	parsed = parse_qs(query)

	return parsed
