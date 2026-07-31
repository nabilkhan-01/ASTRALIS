from typing import cast

from openai import APIError, OpenAI
from openai.types.responses import (
    EasyInputMessageParam,
    ResponseInputItemParam,
)

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
            return self._error(
                "OpenAI API key is not configured.",
            )

        try:
            response = self.client.responses.create(
                model=self.config.openai_model,
                input=self._build_input(
                    conversation,
                ),
            )

            text = response.output_text

            if not text:
                return self._error(
                    "The language provider returned an empty response.",
                )

            return Response(
                text=text,
                success=True,
            )

        except APIError as error:
            status = getattr(
                error,
                "status_code",
                None,
            )

            if status == 429:
                return self._error(
                    "The language service rate limit has been reached. "
                    "Please wait a few moments before trying again.",
                )

            if status == 404:
                return self._error(
                    "The configured language model is unavailable. "
                    "Please verify the configured model name.",
                )

            if status == 503:
                return self._error(
                    "The language service is temporarily unavailable. "
                    "Please try again shortly.",
                )

            return self._error(
                f"Provider error: {error}",
            )

    def _build_input(
        self,
        conversation: Conversation,
    ) -> list[ResponseInputItemParam]:
        """Convert an ASTRALIS conversation into OpenAI input."""

        return cast(
            list[ResponseInputItemParam],
            [
                EasyInputMessageParam(
                    role=message.role.value,
                    content=message.content,
                )
                for message in conversation.messages
            ],
        )

    def _error(
        self,
        message: str,
    ) -> Response:
        """Create an error response."""

        return Response(
            text=message,
            success=False,
        )