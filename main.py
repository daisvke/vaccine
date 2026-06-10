from core.requester import Requester
from core.analyzer import Analyzer
from core.scanner import Scanner
from core.storage import Storage
from utils.parser import parse_args
from injections.boolean import BooleanInjector
from injections.error import ErrorInjector


def main():
	requester = Requester()
	analyzer = Analyzer()
	args = parse_args()
	storage = Storage(args.output)

	boolean = BooleanInjector(requester, analyzer)
	error = ErrorInjector(requester, analyzer)

	scanner = Scanner(requester, analyzer, boolean, error)

	results = scanner.scan(args.url)

	print("\n[*] Results:")
	print(results)

	storage.save({
        "url": args.url,
        "results": results
    })

if __name__ == "__main__":
	main()
