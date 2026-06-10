from utils.logger import Logger


class Analyzer:
	def responses_differ(self, r1: dict, r2: dict):
		Logger.debug(f"Diff: {len(r1.body)},  {len(r2.body)}")

		if r1.status != r2.status:
			return True

		if abs(len(r1.body) - len(r2.body)) > 50:
			return True

		return False

	def has_sql_error(self, response: dict):
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
		return any(e in body for e in errors)
