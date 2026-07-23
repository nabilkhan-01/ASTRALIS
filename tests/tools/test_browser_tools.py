from unittest.mock import patch

from astralis.tools.browser import BrowserTool


class TestBrowserTool:
    """Tests for BrowserTool."""

    @patch("webbrowser.open")
    def test_open(self, mock_open) -> None:
        """Open a website."""

        mock_open.return_value = True

        browser = BrowserTool()

        result = browser.open(
            "https://github.com",
        )

        assert result is True

        mock_open.assert_called_once_with(
            "https://github.com",
        )