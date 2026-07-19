from core.requester import Requester
from core.analyzer import Analyzer
from core.scanner import Scanner
from core.storage import Storage
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

	# Try to login first if login URL is given
	if args.login_url:
		try:
			requester.login(
				args.login_url,
				args.username,
				args.password
			)

		except RuntimeError as e:
			Logger.error(f"Failed to login: {str(e)}")
			sys.exit(1)

	storage = Storage(args.output)
	boolean = BooleanInjector(requester, analyzer)
	error = ErrorInjector(requester, analyzer)
	union = UnionInjector(requester, analyzer)
	scanner = Scanner(requester, analyzer, boolean, error, union)

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
