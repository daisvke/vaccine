import json
import os
from utils.Logger import Logger


class Storage:
	"""This class saves data on a file in JSON format"""
	def __init__(self, filename: str="vaccine.json"):
		self.filename = filename

		if not os.path.exists(self.filename):
			try:
				with open(filename, "w") as f:
					json.dump([], f)
				Logger.success(f"Created `{filename}`")

			except PermissionError:
				Logger.error("Permission denied")

			except OSError as e:
				Logger.error(f"OS error: {e}")
				

	def save(self, data: dict) -> None:
		try:
			with open(self.filename, "r") as f:
				existing = json.load(f)

			existing.append(data)

			with open(self.filename, "w") as f:
				json.dump(existing, f, indent=4)
			
			Logger.success(f"Saved results in `{self.filename}`")

		except FileNotFoundError:
			Logger.error("File does not exist")

		except PermissionError:
			Logger.error("Permission denied")

		except OSError as e:
			Logger.error(f"OS error: {e}")
