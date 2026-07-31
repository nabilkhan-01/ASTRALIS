from unittest.mock import Mock, patch

from astralis.api.search import SearchApi
from astralis.core.config import Config


class TestSearchApi:
    """Tests for the SearchApi."""

    @patch("requests.Session.post")
    def test_search(
        self,
        mock_post: Mock,
    ) -> None:
        """Search the web."""

        response = Mock()

        response.json.return_value = {
            "results": [
                {
                    "title": "Python",
                    "url": "https://python.org",
                    "content": "The official Python website.",
                },
                {
                    "title": "Real Python",
                    "url": "https://realpython.com",
                    "content": "Python tutorials.",
                },
            ],
        }

        response.raise_for_status.return_value = None
        mock_post.return_value = response

        config = Config(
            tavily_api_key="dummy-key",
        )

        api = SearchApi(
            config,
        )

        results = api.search(
            "python",
        )

        mock_post.assert_called_once_with(
            SearchApi.SEARCH_URL,
            timeout=config.api_timeout,
            json={
                "api_key": "dummy-key",
                "query": "python",
                "max_results": 5,
            },
        )

        assert len(results) == 2

        assert results[0].title == "Python"
        assert results[0].url == "https://python.org"
        assert results[0].content == "The official Python website."

        assert results[1].title == "Real Python"
        assert results[1].url == "https://realpython.com"
        assert results[1].content == "Python tutorials."