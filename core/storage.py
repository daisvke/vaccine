import json
import os


class Storage:
    def __init__(self, filename: str="vaccine.json"):
        self.filename = filename

        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump([], f)

    def save(self, data: dict) -> None:
        with open(self.filename, "r") as f:
            existing = json.load(f)

        existing.append(data)

        with open(self.filename, "w") as f:
            json.dump(existing, f, indent=4)
