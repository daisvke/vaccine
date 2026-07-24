from utils.constants import RESET, YELLOW
from utils.parser import extract_params
from core.Requester import Requester
from core.Analyzer import Analyzer
from extractor.BlindExtractor import BlindExtractor
from injections.BooleanInjector import BooleanInjector
from injections.ErrorInjector import ErrorInjector
from injections.UnionInjector import UnionInjector
from injections.TimeInjector import TimeInjector
from utils.Logger import Logger


class Scanner:
	def __init__(self,
			requester: Requester, analyzer: Analyzer,
			boolean: BooleanInjector, error: ErrorInjector,
   			union: UnionInjector, time: TimeInjector,
			extract: BlindExtractor,
		):
		self.requester = requester
		self.analyzer = analyzer
		self.boolean = boolean
		self.error = error
		self.union = union
		self.time = time
		self.extract = extract

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
   

			"""
			Detect context (check how the target SQL query is formed)
   			"""

			# Check if the parameter is quoted or unquoted in the DB query
			context = self.error.detect_context(url, param)
			Logger.success(f"Detected injection context: `{context.name}`")
   
   
			"""
			Determine how many columns are expected by the query.
   			We will need to have the same amount of columns in our query.
   			"""

			column_count = self.union.find_column_count(url, param, context)
			if not column_count:
				Logger.error("Failed to get column count for the SQL query")
				continue
			Logger.success(f"Found column count: {YELLOW}{column_count}{RESET}")

			print()
			Logger.info("Running injections...\n")

			"""
			Run a boolean based test
   			"""

			is_bool = self.boolean.test(url, param, context)
			if is_bool:
				Logger.success(f"Boolean based injection successful!")
				db_name = self.extract.get_db_name(url, param, context, column_count)
				if db_name:
					Logger.success(f"Found database name: {YELLOW}{db_name}{RESET}!\n")
			else:
				Logger.failure(f"Boolean based injection unsuccessful")


			"""
			Run an error based test
   			"""

			payload, database = self.error.test(url, param)
			is_error = True if payload else False
			if is_error:
				Logger.success(f"Error based injection successful!")
			else:
				Logger.failure(f"Error based injection unsuccessful")


			"""
			Run a UNION based test
   			"""

			# db = self.union.test_db_name(url, param)
			db = None
			tables = self.union.test_tables(url, param, context, column_count)
			if tables:
				Logger.success(f"UNION based injection successful!")
				# Logger.debug(tables)
			else:
				Logger.failure(f"UNION based injection unsuccessful")

			is_union = True if db or tables else False


			"""
			Run a time based test
   			"""

			is_time = self.time.test(url, param, context)
			if is_time:
				Logger.success(f"Time based injection successful!")
			else:
				Logger.failure(f"Time based injection unsuccessful")


			"""
			Print results
   			"""

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
				},
    
				"time": {
					"detected": is_time,
				}
			})

		return results
