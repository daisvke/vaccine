class Analyzer:
	def responses_differ(self, r1: dict, r2: dict):
		print(f"Diff: {len(r1.body)},  {len(r2.body)}")

		return len(r1.body) != len(r2.body)

	def has_sql_error(self, response: dict):
		errors = [
			"sql",
			"mysql",
			"sqlite",
			"ora-",
			"syntax error",
			"warning"
		]

		body = response.body.lower()
		return any(e in body for e in errors)
