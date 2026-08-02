from utils.Logger import Logger
from utils.constants import GREEN, RED, RESET


def status(value: bool) -> str:
	if value:
		return f"{GREEN}✓{RESET}"

	return f"{RED}✗{RESET}"

def print_table(table_name: str, columns: dict[str, list[str]]) -> None:
	"""
	Print a dumped table in a readable format.
	"""

	print(f"\nTable: {table_name}")

	if not columns:
		print("(empty)")
		return

	headers = list(columns.keys())
	rows = max(len(values) for values in columns.values())

	# Compute column widths
	widths = []
	for header in headers:
		width = max(
			len(header),
			max((len(str(v)) for v in columns[header]), default=0)
		)
		widths.append(width)

	# Separator
	sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

	# Header
	print(sep)
	print(
		"| "
		+ " | ".join(
			header.ljust(width)
			for header, width in zip(headers, widths)
		)
		+ " |"
	)
	print(sep)

	# Rows
	for i in range(rows):
		print(
			"| "
			+ " | ".join(
				str(columns[header][i]).ljust(width)
				if i < len(columns[header]) else " " * width
				for header, width in zip(headers, widths)
			)
			+ " |"
		)

	print(sep)

def print_results(results: list[dict]) -> None:
	print()
	Logger.success("Results:")

	dump = {}

	detected = sum(
		r["boolean"]["detected"]
		+ r["error"]["detected"]
		+ r["union"]["detected"]
		+ r["time"]["detected"]
		for r in results
	)

	if detected:
		print(f"{RED}Found {detected} vulnerabilit{'ies' if detected > 1 else 'y'}!{RESET}")
	else:
		print(f"{GREEN}No vulnerability found{RESET}")

	def colored_detail(text: str, ok: bool, width: int) -> str:
		color = GREEN if ok else RED
		return f"{color}{text.ljust(width)}{RESET}"

	print("+-----------+----------+--------------------------------------------------------------+")
	print("| Parameter | Test     | Details                                                      |")
	print("+-----------+----------+--------------------------------------------------------------+")

	for result in results:
		param = result["param"]

		"""
		BOOL
  		"""
		bool_detail = colored_detail(
			"✓" if result["boolean"]["detected"] else "✗",
			result["boolean"]["detected"],
			60
		)

		"""
		ERROR
  		"""
		if result["error"]["detected"]:
			# Create a string that lists all the working payloads
			payloads = ", ".join(
				payload
				for payload in result["error"]["payload"]
			)
   
			text = (
				f"✓ {result['error']['database']} "
				f"(payload(s): {payloads})"
			)
		else:
			text = "✗"

		error_detail = colored_detail(
			text,
			result["error"]["detected"],
			60
		)

		"""
		UNION
  		"""
		union_detail = colored_detail(
			"✓" if result["union"]["detected"] else "✗",
			result["union"]["detected"],
			60
		)

		"""
		TIME
  		"""
		time_detail = colored_detail(
			"✓" if result["time"]["detected"] else "✗",
			result["time"]["detected"],
			60
		)
  
		"""
		Print each test
  		"""
		print(
			f"| {param:<9} | {'Boolean':<8} | {bool_detail} |"
		)

		print(
			f"| {'':<9} | {'Error':<8} | {error_detail} |"
		)

		print(
			f"| {'':<9} | {'Union':<8} | {union_detail} |"
		)
  
		print(
			f"| {'':<9} | {'Time':<8} | {time_detail} |"
		)

		print("+-----------+----------+--------------------------------------------------------------+")

		if result["db_dump"]:
			dump = result["db_dump"]

	if dump:
		for db_name, tables in dump.items():
			print(f"\nDatabase: {db_name}")

			for table_name, columns in tables.items():
				print_table(table_name, columns)

def string_to_sql_char(value: str) -> str:
	"""
	Convert a string into a SQL CHAR() expression.

	Example:
	"abc" -> CHAR(97,98,99)
	"""
	ascii_values = ",".join(str(ord(char)) for char in value)

	return f"CHAR({ascii_values})"