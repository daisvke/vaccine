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
	def __init__(
		self, timeout: int=10, method: str="GET", user_agent: str=None
	):
		self.timeout = timeout
		self.method = method.upper()
		self.session = requests.Session()
		user_agent = user_agent or "Vaccine/1.0"
		self.session.headers.update({
			"User-Agent": user_agent
		})
		Logger.info(f"User-Agent: {user_agent}")

	def login(
		self,
		url: str,
		username: str,
		password: str
	) -> None:
		"""Some pages need login"""

		Logger.info("Logging in...")
		response = self.session.post(
			url,
			data={
				"username": username,
				"password": password,
			}
		)

		Logger.debug(response.text)

		if response.status_code != 200:
			raise RuntimeError(
				f"Login failed: HTTP {response.status_code}"
			)
		Logger.success("Successfully logged in")

	def send(
		self,
		url: str,
		params: dict[str, str]=None
	) -> HttpResponse:
		"""Send the HTTP request to the URL"""
		try:
			params = params or {}

			if self.method == "GET":
				r = self.session.get(url, params=params, timeout=self.timeout)
			elif self.method == "POST":
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
			Logger.error(f"Request failed: {e}")
			exit(1)
