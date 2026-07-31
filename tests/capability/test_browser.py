from unittest.mock import Mock

from astralis.capability.browser import BrowserCapability
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestBrowserCapability:
    """Tests for BrowserCapability."""

    @staticmethod
    def _create_capability() -> tuple[BrowserCapability, Mock]:
        """Create a browser capability with a mocked browser."""

        browser = Mock()
        browser.open.return_value = True

        capability = BrowserCapability(
            browser,
        )

        return capability, browser

    def test_open_shortcut(
        self,
    ) -> None:
        """Open a shortcut."""

        capability, browser = self._create_capability()

        response = capability.execute(
            create_request(
                "open github",
            ),
            create_conversation(),
            create_interpretation(
                entities=["browser"],
            ),
        )

        browser.open.assert_called_once_with(
            "https://github.com",
        )

        assert response.success is True
        assert response.text == "Opening https://github.com"

    def test_open_url(
        self,
    ) -> None:
        """Open a URL."""

        capability, browser = self._create_capability()

        response = capability.execute(
            create_request(
                "open python.org",
            ),
            create_conversation(),
            create_interpretation(
                entities=["browser"],
            ),
        )

        browser.open.assert_called_once_with(
            "https://python.org",
        )

        assert response.success is True
        assert response.text == "Opening https://python.org"

    def test_missing_url(
        self,
    ) -> None:
        """Handle a missing URL."""

        capability, _ = self._create_capability()

        response = capability.execute(
            create_request(
                "open",
            ),
            create_conversation(),
            create_interpretation(
                entities=["browser"],
            ),
        )

        assert response.success is False
        assert response.text == "Please specify a website."
