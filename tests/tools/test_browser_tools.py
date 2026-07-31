from unittest.mock import Mock, patch

from astralis.tools.browser import BrowserTool


class TestBrowserTool:
    """Tests for BrowserTool."""

    @staticmethod
    def _create_browser() -> BrowserTool:
        """Create a browser tool."""

        return BrowserTool()

    @patch("webbrowser.open")
    def test_open(
        self,
        mock_open: Mock,
    ) -> None:
        """Open a website."""

        mock_open.return_value = True

        browser = self._create_browser()

        result = browser.open(
            "https://github.com",
        )

        assert result is True

        mock_open.assert_called_once_with(
            "https://github.com",
        )
