from collections.abc import Mapping
from dataclasses import dataclass

import requests

from utils.Logger import Logger


@dataclass
class HttpResponse:
    status: int
    body: str
    headers: Mapping[str, str]
    elapsed: float


class Requester:
    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        method: str = "GET",
        user_agent: str | None = None,
    ):
        self.base_url = base_url
        Logger.debug(f"URL: {self.base_url}")

        self.timeout = timeout
        self.method = method.upper()
        self.session = requests.Session()
        user_agent = user_agent or "Vaccine/1.0"
        self.session.headers.update({"User-Agent": user_agent})
        Logger.info(f"User-Agent: {user_agent}")

    def validateUrl(self) -> bool:
        response = self.send()

        if response.status == 404:
            Logger.error(f"Target not found: {self.base_url}")
            return False

        if response.status >= 500:
            Logger.warning(
                f"Target returned HTTP {response.status}; continuing with analysis..."
            )
            return False

        return True

    def send(self, params: dict[str, str] | None = None) -> HttpResponse:
        """Send the HTTP request to the URL"""

        try:
            params = params or {}

            if self.method == "GET":
                r = self.session.get(self.base_url, params=params, timeout=self.timeout)
            elif self.method == "POST":
                r = self.session.post(self.base_url, data=params, timeout=self.timeout)
            elif self.method == "PATCH":
                r = self.session.patch(self.base_url, data=params, timeout=self.timeout)
            elif self.method == "PUT":
                r = self.session.put(self.base_url, data=params, timeout=self.timeout)
            elif self.method == "DELETE":
                r = self.session.delete(
                    self.base_url, data=params, timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported method: {self.method}")

            return HttpResponse(
                status=r.status_code,
                body=r.text,
                headers=r.headers,
                elapsed=r.elapsed.total_seconds(),
            )

        except requests.RequestException as e:
            Logger.error(f"Request failed: {e}")
            return HttpResponse(status=0, body="", headers={}, elapsed=0)
