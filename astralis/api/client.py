from abc import ABC

import requests


class ApiClient(ABC):
    """Base client for external APIs."""

    def __init__(self) -> None:
        self.session = requests.Session()

    def get(
        self,
        url: str,
        **kwargs,
    ) -> dict:
        """Send a GET request and return JSON."""

        response = self.session.get(
            url,
            timeout=5,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()

    def post(
        self,
        url: str,
        **kwargs,
    ) -> dict:
        """Send a POST request and return JSON."""

        response = self.session.post(
            url,
            timeout=5,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()