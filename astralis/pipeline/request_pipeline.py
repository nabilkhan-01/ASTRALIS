from astralis.brain.brain import Brain
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.monitoring.monitor import Monitor


class RequestPipeline:
    """Coordinates request processing."""

    def __init__(
        self,
        brain: Brain,
        monitor: Monitor,
    ) -> None:
        self.brain = brain
        self.monitor = monitor

    def process(
        self,
        request: Request,
    ) -> Response:
        """Process a request."""

        with self.monitor.measure() as _timer:
            response = self.brain.process(
                request,
            )

        return response