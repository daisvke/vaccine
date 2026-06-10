class Logger:
	RESET = "\033[0m"

	RED = "\033[31m"
	GREEN = "\033[32m"
	YELLOW = "\033[33m"
	BLUE = "\033[34m"

	DEBUG_ENABLED = False

	@staticmethod
	def debug(msg: str) -> None:
		if Logger.DEBUG_ENABLED:
			print(f"[DEBUG] {msg}")

	@staticmethod
	def info(msg: str) -> None:
		print(f"{Logger.BLUE}[INFO]{Logger.RESET} {msg}")

	@staticmethod
	def success(msg: str) -> None:
		print(f"[{Logger.GREEN}*{Logger.RESET}] {msg}")

	@staticmethod
	def warning(msg: str) -> None:
		print(f"{Logger.YELLOW}[WARNING]{Logger.RESET} {msg}")

	@staticmethod
	def error(msg: str) -> None:
		print(f"{Logger.RED}[ERROR]{Logger.RESET} {msg}")
