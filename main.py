from core.Requester import Requester
from core.Analyzer import Analyzer
from core.Scanner import Scanner
from core.Storage import Storage
from extractor.BlindExtractor import BlindExtractor
from injections.TimeInjector import TimeInjector
from utils.parser import parse_args
from injections.BooleanInjector import BooleanInjector
from injections.ErrorInjector import ErrorInjector
from injections.UnionInjector import UnionInjector
from utils.Logger import Logger
from utils.print import print_results


def main():
	args = parse_args()

	if args.debug:
		Logger.DEBUG_ENABLED = True
		Logger.success("Enabled debug mode")

	requester = Requester(user_agent=args.agent)
	analyzer = Analyzer()
	storage = Storage(args.output)
	boolean = BooleanInjector(requester, analyzer)
	error = ErrorInjector(requester, analyzer)
	union = UnionInjector(requester, analyzer)
	time = TimeInjector(requester, analyzer)
	extractor = BlindExtractor(boolean, union)

	scanner = Scanner(requester, analyzer, boolean, error, union, time, extractor)

	# Perform the tests on the URL
	results = scanner.scan(args.url)

	print_results(results)

	# Store the results of the tests on the storage file
	storage.save({
		"url": args.url,
		"method": args.method,
		"results": results
	})

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print()
		Logger.warning("Caught CTRL+C, quitting...")
