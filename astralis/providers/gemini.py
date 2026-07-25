from google import genai
from google.genai import types

from astralis.brain.conversation import Conversation
from astralis.brain.response import Response
from astralis.core.config import Config
from astralis.providers.provider import Provider
from astralis.providers.prompts import SYSTEM_PROMPT


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
        print(f"Model: {self.config.gemini_model}")

    def generate(
        self,
        conversation: Conversation,
    ) -> Response:
        """Generate a response using Google Gemini."""

        if not self.config.gemini_api_key:
            return Response(
                text="Gemini API key is not configured.",
                success=False,
            )

        try:
            response = self.client.models.generate_content(
                model=self.config.gemini_model,
                contents=self._build_contents(conversation),
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                ),
            )

            if not response.text:
                return Response(
                    text="The language provider returned an empty response.",
                    success=False,
                )
            
            return Response(
                text=response.text,
                success=True,
            )

        except Exception as exc:
            message = str(exc)

            if "503" in message:
                return Response(
                    text=(
                        "The language service is temporarily unavailable due to high demand. "
                        "Please try again in a few moments."
                    ),
                    success=False,
                )

            if "404" in message:
                return Response(
                    text=(
                        "The configured language model is unavailable. "
                        "Please verify the configured model name."
                    ),
                    success=False,
                )

            if "429" in message:
                return Response(
                    text=(
                        "The language service rate limit has been reached. "
                        "Please wait a few moments before trying again."
                    ),
                    success=False,
                )
            
            return Response(
                text=f"Provider error: {message}",
                success=False,
            )
    
    
    def _build_contents(
        self,
        conversation: Conversation,
    ) -> list[types.Content]:
        """Convert an ASTRALIS conversation into Gemini content."""

        contents = []

        for message in conversation.messages:
            if message.role.value == "assistant":
                role = "model"
            else:
                role = "user"

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=message.content,
                        )
                    ],
                )
            )

        return contents