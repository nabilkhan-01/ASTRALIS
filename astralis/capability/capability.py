from abc import ABC
from abc import abstractmethod

from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response


class Capability(ABC):
    """Base interface for every ASTRALIS capability."""

    @abstractmethod
    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Execute the capability."""