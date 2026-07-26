from astralis.brain.conversation import Conversation
from astralis.brain.response import Response
from astralis.providers.provider import Provider


class MockProvider(Provider):
    """Simple provider used during early development."""

    def generate(
        self,
        conversation: Conversation,
    ) -> Response:
        """Generate a placeholder response."""

        return Response(
            text="Mock provider response.",
            success=True,
        )
