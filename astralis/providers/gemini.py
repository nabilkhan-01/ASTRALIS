from google import genai
from google.genai import types
from google.genai.errors import APIError

from astralis.brain.conversation import Conversation
from astralis.brain.response import Response
from astralis.brain.role import Role
from astralis.core.config import Config
from astralis.providers.prompts import SYSTEM_PROMPT
from astralis.providers.provider import Provider


class GeminiProvider(Provider):
    """Google Gemini provider implementation."""

    def __init__(
        self,
        config: Config,
    ) -> None:
        self.config = config

        self.client = genai.Client(
            api_key=config.gemini_api_key,
        )

    def generate(
        self,
        conversation: Conversation,
    ) -> Response:
        """Generate a response using Google Gemini."""

        if not self.config.gemini_api_key:
            return self._error(
                "Gemini API key is not configured.",
            )

        try:
            response = self.client.models.generate_content(
                model=self.config.gemini_model,
                contents=self._build_contents(
                    conversation,
                ),
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                ),
            )

            text = response.text

            if not text:
                return self._error(
                    "The language provider returned an empty response.",
                )

            return Response(
                text=text,
                success=True,
            )

        except APIError as error:
            message = str(
                error,
            )

            if "503" in message:
                return self._error(
                    "The language service is temporarily unavailable due to high demand. "
                    "Please try again in a few moments.",
                )

            if "404" in message:
                return self._error(
                    "The configured language model is unavailable. "
                    "Please verify the configured model name.",
                )

            if "429" in message:
                return self._error(
                    "The language service rate limit has been reached. "
                    "Please wait a few moments before trying again.",
                )

            return self._error(
                f"Provider error: {message}",
            )

    def _build_contents(
        self,
        conversation: Conversation,
    ) -> list[types.Content]:
        """Convert an ASTRALIS conversation into Gemini content."""

        contents: list[types.Content] = []

        for message in conversation.messages:
            role = "model" if message.role is Role.ASSISTANT else "user"

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=message.content,
                        ),
                    ],
                ),
            )

        return contents

    def _error(
        self,
        message: str,
    ) -> Response:
        """Create an error response."""

        return Response(
            text=message,
            success=False,
        )
