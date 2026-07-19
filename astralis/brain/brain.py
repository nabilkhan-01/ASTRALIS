from astralis.brain.request import Request
from astralis.brain.response import Response


class Brain:
    """Coordinates intelligence across ASTRALIS."""

    def process(self, request: Request,) -> Response:
        """Process a user request."""

        return Response(
            text="Brain processing is not implemented yet.",
            success=True,
        )