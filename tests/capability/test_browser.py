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

    def setup_method(self) -> None:
        self.capability = BrowserCapability()
        self.capability.browser = Mock()

    def test_open_shortcut(self) -> None:
        """Open a shortcut."""

        response = self.capability.execute(
            create_request(
                "open github",
            ),
            create_conversation(),
            create_interpretation(
                entities=["browser"],
            ),
        )

        assert response.success is True
        assert "https://github.com" in response.text

    def test_open_url(self) -> None:
        """Open a URL."""

        response = self.capability.execute(
            create_request(
                "open python.org",
            ),
            create_conversation(),
            create_interpretation(
                entities=["browser"],
            ),
        )

        assert response.success is True
        assert "https://python.org" in response.text

    def test_missing_url(self) -> None:
        """Handle missing URL."""

        response = self.capability.execute(
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