from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.provider.provider import Provider


class Brain:
    """Coordinates intelligent request processing."""

    def __init__(
        self,
        provider: Provider,
    ) -> None:
        self.provider = provider

    def process(
        self,
        request: Request,
    ) -> Response:
        """Process a user request through the Brain pipeline."""

        # Execute the processing pipeline.
        request = self._validate(request)
        request = self._interpret(request)
        request = self._plan(request)

        return self._execute(request)

    def _validate(
        self,
        request: Request,
    ) -> Request:
        """Validate the incoming request."""

        return request

    def _interpret(
        self,
        request: Request,
    ) -> Request:
        """Interpret the user's request."""

        return request

    def _plan(
        self,
        request: Request,
    ) -> Request:
        """Determine how the request should be handled."""

        return request

    def _execute(
        self,
        request: Request,
    ) -> Response:
        """Execute the processing plan."""

        return self.provider.generate(request)