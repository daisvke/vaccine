from utils.parser import extract_params
from core.requester import Requester
from core.analyzer import Analyzer
from injections.boolean import BooleanInjector
from injections.error import ErrorInjector
from utils.logger import Logger


class Scanner:
	def __init__(self,
			requester: Requester, analyzer: Analyzer,
			boolean: BooleanInjector, error: ErrorInjector
		):
		self.requester = requester
		self.analyzer = analyzer
		self.boolean = boolean
		self.error = error

	def scan(self, url: str):
		params = extract_params(url)
		Logger.debug(f"params: {params}")

		results = []

		for param in params:
			Logger.info(f"Testing {param}")

			is_bool = self.boolean.test(url, param)
			is_error, payload, database = self.error.test(url, param)

			results.append({
				"param": param,
				"boolean": {
					"detected": is_bool,
				},
				"error": {
					"detected": is_error,
					"payload": payload,
					"database": database,
				},
			})

		return results
