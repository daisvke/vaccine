from utils.parser import extract_params
from core.requester import Requester
from core.analyzer import Analyzer
from injections.boolean import BooleanInjector
from injections.error import ErrorInjector
from injections.union import UnionInjector
from utils.logger import Logger


class Scanner:
	def __init__(self,
			requester: Requester, analyzer: Analyzer,
			boolean: BooleanInjector, error: ErrorInjector, union: UnionInjector
		):
		self.requester = requester
		self.analyzer = analyzer
		self.boolean = boolean
		self.error = error
		self.union = union

	def scan(self, url: str):
		params = extract_params(url)

		if params == {}:
			Logger.warning("No params found, exiting...")
			exit(0)
		Logger.debug(f"params: {params}")

		results = []

		for param in params:
			Logger.info(f"Testing {param}")

			# Check if the parameter is quoted or unquoted in the DB query
			context = self.error.detect_context(url, param)
			Logger.success(f"Detected injection context: `{context.name}`")

			is_bool = self.boolean.test(url, param, context)
			is_error, payload, database = self.error.test(url, param)

			db = self.union.test_db_name(url, param)
			tables = self.union.test_tables(url, param)
#			columns = self.union.test_columns(url, param)
			is_union = True if db or tables else False

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

				"union": {
					"detected": is_union,
					"database": db,
					"tables": tables,
				#	"columns": {...},
				#	"dump": [...]
				}
			})

		return results
