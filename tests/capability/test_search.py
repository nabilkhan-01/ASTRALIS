from unittest.mock import Mock

import requests

from astralis.capability.search import SearchCapability
from astralis.core.config import Config
from astralis.models.search_result import SearchResult
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestSearchCapability:
    """Tests for the SearchCapability."""

    def setup_method(self) -> None:
        """Create a SearchCapability."""

        self.capability = SearchCapability(
            Config(
                tavily_api_key="dummy-key",
            ),
        )

        self.capability.api = Mock()

    def test_search(self) -> None:
        """Search the web."""

        self.capability.api.search.return_value = [
            SearchResult(
                title="Python",
                url="https://python.org",
                content="The official Python website.",
            ),
            SearchResult(
                title="Real Python",
                url="https://realpython.com",
                content="Python tutorials.",
            ),
        ]

        response = self.capability.execute(
            create_request(
                "search python",
            ),
            create_conversation(),
            create_interpretation(
                entities=["search"],
            ),
        )

        assert response.success is True

        assert "Python" in response.text
        assert "https://python.org" in response.text
        assert "Real Python" in response.text

    def test_no_results(self) -> None:
        """Handle no search results."""

        self.capability.api.search.return_value = []

        response = self.capability.execute(
            create_request(
                "search python",
            ),
            create_conversation(),
            create_interpretation(
                entities=["search"],
            ),
        )

        assert response.success is True
        assert response.text == "No results found."

    def test_missing_query(self) -> None:
        """Handle a missing search query."""

        response = self.capability.execute(
            create_request(
                "search",
            ),
            create_conversation(),
            create_interpretation(
                entities=["search"],
            ),
        )

        assert response.success is False
        assert response.text == "Please specify a search query."

    def test_api_error(self) -> None:
        """Handle API errors."""

        self.capability.api.search.side_effect = requests.RequestException(
            "Search service unavailable.",
        )

        response = self.capability.execute(
            create_request(
                "search python",
            ),
            create_conversation(),
            create_interpretation(
                entities=["search"],
            ),
        )

        assert response.success is False
        assert response.text == "Search service unavailable."
