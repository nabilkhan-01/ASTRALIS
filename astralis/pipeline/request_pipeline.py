from astralis.brain.brain import Brain
from astralis.brain.context import BrainContext
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.memory.retriever import MemoryRetriever
from astralis.monitoring.monitor import Monitor


class RequestPipeline:
    """Coordinates request processing."""

    def __init__(
        self,
        brain: Brain,
        retriever: MemoryRetriever,
        monitor: Monitor,
    ) -> None:
        self._brain = brain
        self._retriever = retriever
        self._monitor = monitor

    def process(
        self,
        request: Request,
    ) -> Response:
        """Process a request."""

        with self._monitor.measure() as _timer:
            context = self._retriever.retrieve(
                request,
            )

            brain_context = BrainContext(
                request=request,
                context=context,
            )

            response = self._brain.process(
                brain_context,
            )

        return response