from abc import ABC, abstractmethod

from astralis.brain.conversation import Conversation
from astralis.brain.response import Response


class Provider(ABC):
    """Base class for AI providers."""

    @abstractmethod
    def generate(
        self,
        conversation: Conversation,
    ) -> Response:
        """Generate a response."""
