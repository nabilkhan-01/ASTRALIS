from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.providers.provider import Provider


class LanguageCapability(Capability):
    """Handles natural language generation."""

    def __init__(
        self,
        provider: Provider,
    ) -> None:
        self.provider = provider

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Generate a response using the configured language provider."""

        return self.provider.generate(
            conversation,
        )
