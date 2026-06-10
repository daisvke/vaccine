from core.requester import Requester
from core.analyzer import Analyzer


class BooleanInjector:
	def __init__(self, requester: Requester, analyzer: Analyzer):
		self.requester = requester
		self.analyzer = analyzer

	def test(self, url: str, param: dict):
		r_true = self.requester.send(
			url, "GET", {param: "1 AND 1=1"}
		)

		r_false = self.requester.send(
			url, "GET", {param: "1 AND 1=2"}
		)

		# print(r_true)

		return self.analyzer.responses_differ(r_true, r_false)
