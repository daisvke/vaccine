from core.Requester import HttpResponse
from utils.Logger import Logger


DATABASE_ERRORS = {
	"Microsoft SQL Server": [
		"unclosed quotation mark",
		"microsoft sql server",
		"sql server"
	],

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
}


class Analyzer:
	def responses_differ(self, r1: HttpResponse, r2: HttpResponse, diff: int) -> bool:
		# Logger.debug(r1.body)
		# Logger.debug(r2.body)
		# Logger.debug(f"Diff: {len(r1.body)},  {len(r2.body)}")

		if r1.status != r2.status:
			return True

		if abs(len(r1.body) - len(r2.body)) > diff:
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
			"warning",
   			"the used select statements have a different number of columns",
      		"unknown column",
		]

		body = response.body.lower()
#		Logger.debug(f"body: {body}")
		return any(e in body for e in errors)
			
	def is_delayed(self, r_normal: HttpResponse, r_sleep: HttpResponse, sleep: int):
		return (
			r_sleep.elapsed - r_normal.elapsed >= sleep - 0.5
		)