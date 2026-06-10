from utils.parser import extract_params
from core.requester import Requester
from core.analyzer import Analyzer
from injections.boolean import BooleanInjector
from injections.error import ErrorInjector

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
		print(f"params: {params}")

		results = []

		for param in params:
			print(f"[*] Testing {param}")

			is_bool = self.boolean.test(url, param)
			is_error = self.error.test(url, param)

			if is_bool or is_error:
				results.append({
					"param": param,
					"boolean": is_bool,
					"error": is_error,
				})

		return results
