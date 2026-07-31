from abc import ABC
from typing import Any

import requests

from astralis.core.config import Config


class ApiClient(ABC):
    """Base client for external APIs."""

    def __init__(
        self,
        config: Config,
    ) -> None:
        self.config = config
        self.session = requests.Session()
        self.timeout = config.api_timeout

        self.session.headers.update(
            {
                "User-Agent": config.user_agent,
                "Accept": "application/json",
            },
        )

    def get(
        self,
        url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Send a GET request and return JSON."""

        response = self.session.get(
            url,
            timeout=self.timeout,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()

    def post(
        self,
        url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Send a POST request and return JSON."""

        response = self.session.post(
            url,
            timeout=self.timeout,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()
