from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.provider.provider import Provider


class MockProvider(Provider):
    """Simple provider used during early development."""

    def generate(
        self,
        request: Request,
    ) -> Response:
        """Generate a placeholder response."""

        return Response(
            text="Mock provider response.",
            success=True,
        )