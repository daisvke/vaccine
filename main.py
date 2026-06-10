from core.requester import Requester
from core.analyzer import Analyzer
from core.scanner import Scanner
from core.storage import Storage

from injections.boolean import BooleanInjector
from injections.error import ErrorInjector


def main():
	url = "http://192.168.56.101/index.php?page=member&id=1+and+1%3D2&Submit=Submit#"
	requester = Requester()
	analyzer = Analyzer()

	boolean = BooleanInjector(requester, analyzer)
	error = ErrorInjector(requester, analyzer)

	scanner = Scanner(requester, analyzer, boolean, error)

	results = scanner.scan(url)

	print("\n[*] Results:")
	print(results)

if __name__ == "__main__":
	main()
