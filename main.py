from core.requester import Requester
from core.analyzer import Analyzer
from core.scanner import Scanner
from core.storage import Storage
from utils.parser import parse_args
from injections.boolean import BooleanInjector
from injections.error import ErrorInjector
from utils.logger import Logger


def print_results(results: list[dict]) -> None:
	headers = ["Parameter", "Boolean", "Error"]

	print(f"\n{headers[0]:<15}{headers[1]:<10}{headers[2]:<10}")
	print("-" * 35)

	for r in results:
		print(
			f"{r['param']:<15}"
			f"{str(r['boolean']):<10}"
			f"{str(r['error']):<10}"
		)
	print()


def main():
	args = parse_args()
	requester = Requester(user_agent=args.agent)
	analyzer = Analyzer()
	storage = Storage(args.output)
	boolean = BooleanInjector(requester, analyzer)
	error = ErrorInjector(requester, analyzer)
	scanner = Scanner(requester, analyzer, boolean, error)

	if args.debug:
		Logger.DEBUG_ENABLED = True
		Logger.success("Enabled debug mode")

	# Perform the tests on the URL
	results = scanner.scan(args.url)

	print()
	Logger.success("Results:")
	if results != []:
		print(Logger.RED + "Found vulnerabilities!" + Logger.RESET)
	else:
		print(Logger.GREEN + "No vulnerability found" + Logger.RESET)
	print_results(results)

	# Store the results of the tests on the storage file
	storage.save({
		"url": args.url,
		"method": args.method,
		"results": results
	})

if __name__ == "__main__":
	main()
