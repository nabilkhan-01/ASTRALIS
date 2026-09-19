from typing import Any

import requests

from astralis.brain.conversation import Conversation
from astralis.brain.response import Response
from astralis.brain.role import Role
from astralis.providers.local import LocalProvider
from astralis.providers.prompts import SYSTEM_PROMPT
from astralis.providers.reasoning import ReasoningMode


class OllamaProvider(LocalProvider):
    """Ollama local AI model provider implementation."""

    def __init__(
        self,
        model: str,
        host: str = LocalProvider.DEFAULT_HOST,
        timeout: int = 60,
        reasoning_mode: ReasoningMode = ReasoningMode.AUTO,
    ) -> None:
        super().__init__(
            model=model,
            host=host,
        )
        self.timeout = timeout
        self.reasoning_mode = reasoning_mode

    def _resolve_think_parameter(
        self,
    ) -> bool:
        """Resolve the top-level 'think' API parameter for Ollama.

        - FAST: Explicitly disable extended reasoning (think=False).
        - DEEP: Explicitly enable extended reasoning (think=True).
        - AUTO: Default mode; safely uses fast local inference (think=False)
          until task-aware routing is introduced in a later v0.5.0 step.
        """

        # DEEP enables extended thinking; FAST and AUTO safely use fast local inference.
        return self.reasoning_mode is ReasoningMode.DEEP

    def generate(
        self,
        conversation: Conversation,
    ) -> Response:
        """Generate a response using the Ollama local HTTP API."""

        if not self.model:
            return Response(
                text="Ollama model is not configured. Please set OLLAMA_MODEL.",
                success=False,
            )

        endpoint = f"{self.host}/api/chat"
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(
                conversation,
            ),
            "stream": False,
            "think": self._resolve_think_parameter(),
        }


        try:
            http_response = requests.post(
                endpoint,
                json=payload,
                timeout=self.timeout,
            )

            if not http_response.ok:
                error_detail = self._extract_error(
                    http_response,
                )
                return Response(
                    text=f"Ollama error: {error_detail}",
                    success=False,
                )

            data = http_response.json()
            message = data.get("message", {})
            text = message.get("content")

            if not text:
                return Response(
                    text="The language provider returned an empty response.",
                    success=False,
                )

            return Response(
                text=text,
                success=True,
            )

        except requests.exceptions.RequestException as error:
            return self._connection_error(
                details=str(error),
            )

    def _build_messages(
        self,
        conversation: Conversation,
    ) -> list[dict[str, str]]:
        """Convert an ASTRALIS conversation into Ollama chat messages.

        Ensures exactly one system prompt is sent at the start of the payload
        and is not duplicated into conversation history.
        """

        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
        ]

        for message in conversation.messages:
            if message.role is Role.SYSTEM:
                continue

            messages.append(
                {
                    "role": message.role.value,
                    "content": message.content,
                },
            )

        return messages

    @staticmethod
    def _extract_error(
        response: requests.Response,
    ) -> str:
        """Extract error details from an Ollama HTTP response."""

        try:
            data = response.json()
        except ValueError:
            return response.text or f"HTTP {response.status_code}"

        if isinstance(data, dict) and "error" in data:
            return str(data["error"])

        return response.text or f"HTTP {response.status_code}"
