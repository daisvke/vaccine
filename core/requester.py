import requests
from dataclasses import dataclass
from utils.logger import Logger


@dataclass
class HttpResponse:
	status: int
	body: str
	headers: dict
	elapsed: float


class Requester:
	def __init__(self, timeout=10, user_agent=None):
		self.timeout = timeout
		self.session = requests.Session()
		user_agent = user_agent or "Vaccine/1.0"
		self.session.headers.update({
			"User-Agent": user_agent
		})
		Logger.info(f"User-Agent: {user_agent}")

	def send(self, url: str, method: str="GET", params: dict[str, str]=None) -> HttpResponse:
		try:
			params = params or {}
			method = method.upper()

			if method == "GET":
				r = self.session.get(url, params=params, timeout=self.timeout)
			elif method == "POST":
				r = self.session.post(url, data=params, timeout=self.timeout)
			else:
				raise ValueError(
					f"Unsupported method: {method}"
				)
				
			return HttpResponse(
				status=r.status_code,
				body=r.text,
				headers=r.headers,
				elapsed=r.elapsed.total_seconds()
			)
			
		except requests.RequestException as e:
			raise RuntimeError(
				f"Request failed: {e}"
			) from e
