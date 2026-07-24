from core.Requester import Requester, HttpResponse
from core.Analyzer import Analyzer
from utils.Logger import Logger
from utils.constants import InjectionContext

class ErrorInjector:
	"""
	Error SQLi relies on database error messages.
 	"""
 
	def __init__(self, requester: Requester, analyzer: Analyzer):
		self.requester = requester
		self.analyzer = analyzer

	def detect_context(self, url, param):
		"""
		Determine the prefix and suffix of our SQL queries according to the
		way the target query is formed.
  		"""
  
		Logger.info("Context detection...")
		response = self.requester.send(url, {param: "1'"})
		#Logger.debug(response)

		if self.analyzer.has_sql_error(response):
			Logger.info("Detected SQL error message with quote in the parameter...")
   
			response = self.requester.send(url, {param: "1' -- -"})
			if not self.analyzer.has_sql_error(response):
				Logger.info("SQL error is avoided with commenting trailing characters...")

				return InjectionContext(
					prefix="1' ",
					suffix=" -- -",
					name="quoted"
				)

		return InjectionContext(
			prefix="1 ",
			suffix="",
			name="unquoted"
		)

	def test(self, url: str, param: str) -> tuple[list[str] | None, str | None]:
		"""
		Test the different payloads to check if they produce SQL error messages.
		If they do, it would mean that the injection has worked.
  		"""
  
		payloads = ["'", '"', "'", "1' -- -", "1'"]
		payloads_success = []  # payload which injection worked
		database = None

		for p in payloads:
			response = self.requester.send(url, {param: p})
			# Logger.debug(f"payload: {p}")

			if self.analyzer.has_sql_error(response):
				if not database:
					database = self.analyzer.detect_database(response.body)
				payloads_success.append(p)

		return payloads_success, database

