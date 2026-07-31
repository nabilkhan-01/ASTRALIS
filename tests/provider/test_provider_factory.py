from astralis.brain.conversation import Conversation
from astralis.providers.mock import MockProvider


class TestMockProvider:
    """Tests for the MockProvider."""

    @staticmethod
    def _create_provider() -> MockProvider:
        """Create a mock provider."""

        return MockProvider()

    def test_generate(
        self,
    ) -> None:
        """Generate a mock response."""

        provider = self._create_provider()

        response = provider.generate(
            Conversation(),
        )

        assert response.success is True
        assert response.text == "Mock provider response."
