from abc import ABC, abstractmethod

from astralis.brain.request import Request
from astralis.brain.response import Response


class Provider(ABC):
    """Defines the interface for AI providers."""

    @abstractmethod
    def generate(
        self,
        request: Request,
    ) -> Response:
        """Generate a response for a request."""