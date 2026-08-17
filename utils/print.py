from utils.constants import BLUE, BOLD, CYAN, GREEN, RED, RESET, YELLOW
from utils.Logger import Logger


def status(value: bool) -> str:
    if value:
        return f"{GREEN}✓{RESET}"

    return f"{RED}✗{RESET}"


def print_table(table_name: str, columns: dict) -> None:
    """Print a dumped table with column metadata in headers."""

    print(f"\n{BOLD}{BLUE}Table: {CYAN}{table_name}{RESET}")

    if not columns:
        print(f"{YELLOW}(empty){RESET}")
        return

    # Build headers and collect values.
    plain_headers = []
    values = {}

    for column_name, info in columns.items():
        data_type = info.get("data_type", "unknown")
        max_length = info.get("character_maximum_length")

        meta = data_type
        if max_length is not None:
            meta += f",{max_length}"

        plain_headers.append(f"{column_name} ({meta})")
        values[column_name] = info.get("values", [])

    row_count = max((len(v) for v in values.values()), default=0)

    rows = []
    for i in range(row_count):
        rows.append(
            [
                str(values[column][i]) if i < len(values[column]) else ""
                for column in columns
            ]
        )

    # Calculate widths using uncolored text.
    widths = [
        max(
            len(plain_headers[i]),
            max((len(row[i]) for row in rows), default=0),
        )
        for i in range(len(plain_headers))
    ]

    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    print(separator)
    print(
        "| "
        + " | ".join(
            plain_headers[i].ljust(widths[i]) for i in range(len(plain_headers))
        )
        + " |"
    )
    print(separator)

    for row in rows:
        print(
            "| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(row))) + " |"
        )

    print(separator)


def print_results(data: dict) -> None:
    print()
    Logger.success("Results:")

    dump = {}

    results = data.get("results", [])
    method = data.get("method", "GET")

    detected = sum(
        r["boolean"]["detected"]
        + r["error"]["detected"]
        + r["union"]["detected"]
        + r["time"]["detected"]
        for r in results
    )

    if detected:
        Logger.success(
            f"Found {detected} SQL injection technique{'s' if detected > 1 else ''}!"
        )
    else:
        Logger.success("No SQL injection technique found")

    def colored_detail(text: str, ok: bool, width: int) -> str:
        color = GREEN if ok else RED
        return f"{color}{text.ljust(width)}{RESET}"

    print(
        "+-----------+--------+----------+--------------------------------------------------------------+"
    )
    print(
        "| Parameter | Method | Test     | Details                                                      |"
    )
    print(
        "+-----------+--------+----------+--------------------------------------------------------------+"
    )

    for result in results:
        param = result.get("param", "UNKNOWN")
        boolean = result.get("boolean", {})
        error = result.get("error", {})
        union = result.get("union", {})
        time = result.get("time", {})

        bool_detected = boolean.get("detected", False)
        error_detected = error.get("detected", False)
        union_detected = union.get("detected", False)
        time_detected = time.get("detected", False)

        """
		BOOL
  		"""
        bool_detail = colored_detail(
            "✓" if bool_detected else "✗",
            bool_detected,
            60,
        )

        """
		ERROR
  		"""
        if error_detected:
            # Create a string that lists all the working payloads
            payloads = ", ".join(payload for payload in result["error"]["payload"])
            database = error.get("database", "unknown")
            text = f"✓ {database} (payload(s): {payloads})"
        else:
            text = "✗"

        error_detail = colored_detail(text, result["error"]["detected"], 60)

        """
		UNION
  		"""
        union_detail = colored_detail(
            "✓" if union_detected else "✗", union_detected, 60
        )

        """
		TIME
  		"""
        time_detail = colored_detail("✓" if time_detected else "✗", time_detected, 60)

        """
		Print each test
  		"""
        print(
            f"| {CYAN}{param:<9}{RESET} | "
            f"{YELLOW}{method:<6}{RESET} | "
            f"{BLUE}{'Boolean':<8}{RESET} | {bool_detail} |"
        )

        print(f"| {'':<9} | {'':<6} | {BLUE}{'Error':<8}{RESET} | {error_detail} |")

        print(f"| {'':<9} | {'':<6} | {BLUE}{'Union':<8}{RESET} | {union_detail} |")

        print(f"| {'':<9} | {'':<6} | {BLUE}{'Time':<8}{RESET} | {time_detail} |")

        print(
            "+-----------+--------+----------+--------------------------------------------------------------+"
        )

        if result.get("db_dump"):
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
