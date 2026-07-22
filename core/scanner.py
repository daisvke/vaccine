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
			print('\n')
			Logger.info(f"---------- Testing parameter: `{param}` ----------\n")

			# Check if the parameter is quoted or unquoted in the DB query
			context = self.error.detect_context(url, param)
			Logger.success(f"Detected injection context: `{context.name}`")

			column_count = self.union.find_column_count(url, param, context)
			if not column_count:
				Logger.error("Failed to get column count for the SQL query")
				continue
			Logger.success(f"Found column count: {column_count}")
    
			is_bool = self.boolean.test(url, param, context)
			if is_bool:
				Logger.success(f"Boolean based injection successful!")
				
			payload, database = self.error.test(url, param)
			is_error = True if payload else False
			if is_error:
				Logger.success(f"Error based injection successful!")

			# db = self.union.test_db_name(url, param)
			db = None
			tables = self.union.test_tables(url, param, context, column_count)
			Logger.success(f"Union based injection successful!")
			# if tables:
				# Logger.debug(tables)
				
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
