from openai import OpenAI

from astralis.brain.conversation import Conversation
from astralis.brain.response import Response
from astralis.core.config import Config
from astralis.providers.provider import Provider


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
        conversation: Conversation,
    ) -> Response:
        """Generate a response using OpenAI."""

        if not self.config.openai_api_key:
            return Response(
                text="OpenAI API key is not configured.",
                success=False,
            )

        try:
            response = self.client.responses.create(
                model=self.config.openai_model,
                input=conversation.messages[-1].content,
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