from sys import exit
from urllib.parse import urlparse

from core.Analyzer import Analyzer
from core.Requester import Requester
from core.Scanner import Scanner
from core.Storage import Storage
from extractor.BlindExtractor import BlindExtractor
from injections.BooleanInjector import BooleanInjector
from injections.ErrorInjector import ErrorInjector
from injections.TimeInjector import TimeInjector
from injections.UnionInjector import UnionInjector
from utils.Logger import Logger
from utils.parse import parse_args
from utils.print import print_results


def main():
    args = parse_args()

    if args.debug:
        Logger.DEBUG_ENABLED = True
        Logger.success("Enabled debug mode")

    base_url = urlparse(args.url)._replace(query="").geturl()

    requester = Requester(base_url, method=args.method, user_agent=args.agent)
    if not requester.validateUrl():  # Check if baseline URL is reachable
        exit(1)

    analyzer = Analyzer()
    storage = Storage(args.output)
    boolean = BooleanInjector(requester, analyzer)
    error = ErrorInjector(requester, analyzer)
    union = UnionInjector(requester, analyzer)
    time = TimeInjector(requester, analyzer)
    extractor = BlindExtractor(time, boolean, union)

    scanner = Scanner(
        base_url,
        args.method,
        requester,
        analyzer,
        boolean,
        error,
        union,
        time,
        extractor,
    )

    # Perform the tests on the URL
    params_count, results = scanner.scan(args.url)

    print_results(results)

    # Store the results of the tests on the storage file
    storage.save(params_count, results)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        Logger.warning("Caught CTRL+C, quitting...")
