from unittest import result

from astralis.api.client import ApiClient
from astralis.models.search_result import SearchResult
from astralis.core.config import Config


class SearchApi(ApiClient):
    """Client for searching the web using Tavily."""

    SEARCH_URL = "https://api.tavily.com/search"

    def __init__(
        self,
        config: Config,
    ) -> None:
        super().__init__()

        self.config = config

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        """Search the web."""

        if not self.config.tavily_api_key:
            raise ValueError("Tavily API key is not configured.",
            )
        data = self.post(
            self.SEARCH_URL,
            json={
                "api_key": self.config.tavily_api_key,
                "query": query,
                "max_results": max_results,
            },
        )

        return [
            SearchResult(
                title=result.get("title", ""),
                url=result.get("url", ""),
                content=result.get("content", ""),
            )
            for result in data.get("results", [])
        ]