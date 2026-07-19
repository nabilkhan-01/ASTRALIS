from google import genai

from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.core.config import Config
from astralis.provider.provider import Provider


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
        request: Request,
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
                contents=request.text,
            )

            return Response(
                text=response.text,
                success=True,
            )

        except Exception as exc:
            return Response(
                text=f"Provider error: {exc}",
                success=False,
            )