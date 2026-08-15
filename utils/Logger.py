from utils.constants import BLUE, GREEN, RED, RESET, YELLOW


class Logger:
    DEBUG_ENABLED: bool = False

    @staticmethod
    def debug(msg: str) -> None:
        if Logger.DEBUG_ENABLED:
            print(f"[DEBUG] {msg}")

    @staticmethod
    def info(msg: str) -> None:
        print(f"{BLUE}[INFO]{RESET} {msg}")

    @staticmethod
    def success(msg: str) -> None:
        print(f"[{GREEN}*{RESET}] {msg}")

    @staticmethod
    def failure(msg: str) -> None:
        print(f"[{RED}x{RESET}] {msg}")

    @staticmethod
    def warning(msg: str) -> None:
        print(f"{YELLOW}[WARNING]{RESET} {msg}")

    @staticmethod
    def error(msg: str) -> None:
        print(f"{RED}[ERROR]{RESET} {msg}")
