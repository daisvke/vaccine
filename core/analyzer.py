from core.requester import HttpResponse
from utils.logger import Logger


DATABASE_ERRORS = {
	"MariaDB": [
		"mariadb"
	],

	"MySQL": [
		"you have an error in your sql syntax",
		"mysql"
	],

	"SQLite": [
		"sqlite",
		"sqlite3::"
	],

	"Oracle": [
		"ora-",
		"oracle error"
	],

	"Microsoft SQL Server": [
		"unclosed quotation mark",
		"microsoft sql server",
		"sql server"
	]
}


class Analyzer:
	def responses_differ(self, r1: HttpResponse, r2: HttpResponse) -> bool:
		# Logger.debug(r1.body)
		# Logger.debug(r2.body)
		Logger.debug(f"Diff: {len(r1.body)},  {len(r2.body)}")

		if r1.status != r2.status:
			return True

		if abs(len(r1.body) - len(r2.body)) > 50:
			return True

		return False

	def detect_database(self, response_body: str) -> str:
		body = response_body.lower()

		for database, signatures in DATABASE_ERRORS.items():
			for signature in signatures:
				if signature in body:
					return database

		return "Unknown"

	def has_sql_error(self, response: HttpResponse):
		errors = [
			"mariadb",
			"sql",
			"mysql",
			"sqlite",
			"ora-",
			"syntax error",
			"warning"
		]

		body = response.body.lower()
#		Logger.debug(f"body: {body}")
		return any(e in body for e in errors)
			
