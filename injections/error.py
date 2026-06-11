from core.requester import Requester, HttpResponse
from core.analyzer import Analyzer


class ErrorInjector:
	def __init__(self, requester: Requester, analyzer: Analyzer):
		self.requester = requester
		self.analyzer = analyzer

	def test(self, url: str, param: dict) -> tuple[bool, str | None, str | None]:
		payloads = ["'", '"', "1'"]

		for p in payloads:
			response = self.requester.send(url, "GET", {param: p})

			if self.analyzer.has_sql_error(response):
				return True, p, self.analyzer.detect_database(response.body)

		return False, None, None

