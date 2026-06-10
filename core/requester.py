import requests
from dataclasses import dataclass


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
		self.session.headers.update({
			"User-Agent": user_agent or "Vaccine/1.0"
		})

	def send(self, url: str, method: str="GET", params: dict=None) -> dict:
		params = params or {}
		method = method.upper()

		if method == "GET":
			r = self.session.get(url, params=params, timeout=self.timeout)
		else:
			r = self.session.post(url, data=params, timeout=self.timeout)

		return HttpResponse(
			status=r.status_code,
			body=r.text,
			headers=r.headers,
			elapsed=r.elapsed.total_seconds()
		)
