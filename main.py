from core.requester import Requester
from core.analyzer import Analyzer
from core.scanner import Scanner
from core.storage import Storage
from injections.time import TimeInjector
from utils.parser import parse_args
from injections.boolean import BooleanInjector
from injections.error import ErrorInjector
from injections.union import UnionInjector
from utils.logger import Logger
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

	scanner = Scanner(requester, analyzer, boolean, error, union, time)

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
	main()
