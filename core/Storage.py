import json
import os

from utils.Logger import Logger


class Storage:
    """This class saves data on a file in JSON format"""

    def __init__(self, filename: str = "vaccine.json"):
        self.filename = filename
        self.count = 0

        if not os.path.exists(self.filename):
            try:
                with open(filename, "w") as f:
                    json.dump([], f)
                Logger.success(f"Created `{filename}`")

            except PermissionError:
                Logger.error("Permission denied")

            except OSError as e:
                Logger.error(f"OS error: {e}")
        else:
            existing = self.get_data()
            for result in existing:
                id = result.get("id", 0)
                self.count = max(self.count, id)

    def get_data(self) -> list[dict]:
        try:
            with open(self.filename, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        except FileNotFoundError:
            Logger.error("File does not exist")

        except PermissionError:
            Logger.error("Permission denied")

        except OSError as e:
            Logger.error(f"OS error: {e}")
        return []

    def save(self, param_count: int, data: dict) -> None:
        try:
            existing = self.get_data()
            existing.append({"id": self.count + 1, **data})

            with open(self.filename, "w") as f:
                json.dump(existing, f, indent=4)

            Logger.success(f"Saved results in `{self.filename}`")

        except FileNotFoundError:
            Logger.error("File does not exist")

        except PermissionError:
            Logger.error("Permission denied")

        except OSError as e:
            Logger.error(f"OS error: {e}")
