from utils.constants import HEIGH_ELEMENT_COUNT, RESET, YELLOW
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
  
		self.results: list = []

	def scan(self, url: str):
		params = extract_params(url)

		if params == {}:
			Logger.warning("No params found, exiting...")
			exit(0)
		Logger.debug(f"params: {params}")

		for param in params:
			print()
			Logger.info(f"---------- Testing parameter: `{param}` ----------\n")

			print()
			Logger.info("Running injections...\n")


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
   

			"""
			Run a UNION based test
   			"""

			is_union = self.union.test_marker(url, param, context, column_count)
			if is_union:
				Logger.success(f"UNION based injection successful!")
				# Logger.debug(tables)
			else:
				Logger.failure(f"UNION based injection unsuccessful")


			"""
			Run a boolean based test
   			"""

			is_bool = self.boolean.test(url, param, context)
			db_dump = {}

			if is_bool:
				Logger.success(f"Boolean based injection successful!")
				if is_union:
					do_dump = input("Do you want to perform a database dump? (y/n): ")

					if do_dump.lower() == "y":
						# Create a NULL list matching the number of columns to make query compatible.
						# We substract 1 from count because the main element is added afterwards 
						nulls = ",".join(["NULL"] * (column_count - 1))
						db_dump = self.extract.dump_db_entries(url, param, context, column_count, nulls)

			else:
				Logger.failure(f"Boolean based injection unsuccessful")


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

			self.results.append({
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
				},
    
				"time": {
					"detected": is_time,
				},
    
				"db_dump": db_dump
			})

		return self.results
