from astralis.brain.conversation import Conversation
from astralis.providers.mock import MockProvider


class TestMockProvider:
    """Tests for the MockProvider."""

    def setup_method(self) -> None:
        """Create a mock provider."""

        self.provider = MockProvider()

    def test_generate(self) -> None:
        """Generate a mock response."""

        conversation = Conversation()

        response = self.provider.generate(
            conversation,
        )

        assert response.success is True
        assert response.text == "Mock provider response."

    def test_empty_conversation(self) -> None:
        """Support empty conversations."""

        response = self.provider.generate(
            Conversation(),
        )

        assert response.success is True
        assert response.text == "Mock provider response."
