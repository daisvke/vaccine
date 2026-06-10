from core.requester import Requester
from core.analyzer import Analyzer


class ErrorInjector:
    def __init__(self, requester: Requester, analyzer: Analyzer):
        self.requester = requester
        self.analyzer = analyzer

    def test(self, url: str, param: dict):
        payloads = ["'", '"', "1'"]

        for p in payloads:
            r = self.requester.send(url, "GET", {param: p})

            if self.analyzer.has_sql_error(r):
                return True

        return False

