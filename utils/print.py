from utils.logger import Logger
from utils.constants import GREEN, RED, RESET


def status(value: bool) -> str:
	if value:
		return f"{GREEN}✓{RESET}"

	return f"{RED}✗{RESET}"


def print_results(results: list[dict]) -> None:
	print()

	Logger.success("Results:")

	detected = 0
	detected = sum(
		r["boolean"]["detected"] + r["error"]["detected"] + r["union"]["detected"]
		for r in results
	)

	if detected:
		print(f"{RED}Found {detected} vulnerabilit{'ies' if detected > 1 else 'y'}!{RESET}")
	else:
		print(f"{GREEN}No vulnerability found{RESET}")

	def colored_detail(text: str, ok: bool, width: int) -> str:
		color = GREEN if ok else RED
		return f"{color}{text.ljust(width)}{RESET}"


	print("+-----------+----------+--------------------------------------+")
	print("| Parameter | Test     | Details                              |")
	print("+-----------+----------+--------------------------------------+")

	for result in results:
		param = result["param"]

		bool_detail = colored_detail(
			"✓" if result["boolean"]["detected"] else "✗",
			result["boolean"]["detected"],
			36
		)

		if result["error"]["detected"]:
			text = (
				f"✓ {result['error']['database']} "
				f"(payload: {result['error']['payload']})"
			)
		else:
			text = "✗"

		error_detail = colored_detail(
			text,
			result["error"]["detected"],
			36
		)

		union_detail = colored_detail(
			"✓" if result["union"]["detected"] else "✗",
			result["union"]["detected"],
			36
		)

		print(
			f"| {param:<9} | {'Boolean':<8} | {bool_detail} |"
		)

		print(
			f"| {'':<9} | {'Error':<8} | {error_detail} |"
		)

		print(
			f"| {'':<9} | {'Union':<8} | {union_detail} |"
		)

		print("+-----------+----------+--------------------------------------+")
