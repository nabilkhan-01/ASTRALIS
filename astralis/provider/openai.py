from openai import OpenAI

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
        self.client = OpenAI(
            api_key=config.openai_api_key,
        )

    def generate(
        self,
        request: Request,
    ) -> Response:
        """Generate a response using OpenAI."""

        if not self.config.openai_api_key:
            return Response(
                text="OpenAI API key is not configured.",
                success=False,
            )

        try:
            response = self.client.responses.create(
                model=self.config.model,
                input=request.text,
            )

            return Response(
                text=response.output_text,
                success=True,
            )

        except Exception as exc:
            return Response(
                text=f"Provider error: {exc}",
                success=False,
            )