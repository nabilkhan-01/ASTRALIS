from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.core.config import Config
from astralis.provider.provider import Provider


class OpenAIProvider(Provider):
    """OpenAI provider implementation."""

    def __init__(
        self,
        config: Config,
    ) -> None:
        self.config = config

    def generate(
        self,
        request: Request,
    ) -> Response:
        """Generate a response using OpenAI."""

        return Response(
            text="OpenAI provider is not configured yet.",
            success=False,
        )