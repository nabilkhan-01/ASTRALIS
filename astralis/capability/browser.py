from typing import ClassVar

from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.tools.browser import BrowserTool


class BrowserCapability(Capability):
    """Opens websites in the default browser."""

    SHORTCUTS: ClassVar[dict[str, str]] = {
        "google": "https://www.google.com",
        "github": "https://github.com",
        "youtube": "https://www.youtube.com",
        "openai": "https://openai.com",
    }

    def __init__(
        self,
        browser: BrowserTool,
    ) -> None:
        self.browser = browser

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Open a website."""

        _ = conversation, interpretation

        try:
            url = self._extract_url(
                request.text,
            )

        except ValueError as error:
            return Response(
                text=str(error),
                success=False,
            )

        if not self.browser.open(
            url,
        ):
            return Response(
                text="Failed to open the browser.",
                success=False,
            )

        return Response(
            text=f"Opening {url}",
        )

    def _extract_url(
        self,
        text: str,
    ) -> str:
        """Extract the requested URL."""

        text = text.strip()

        if not text.lower().startswith(
            "open ",
        ):
            raise ValueError(
                "Please specify a website.",
            )

        target = text[5:].strip().lower()

        if not target:
            raise ValueError(
                "Please specify a website.",
            )

        if target in self.SHORTCUTS:
            return self.SHORTCUTS[target]

        if not target.startswith(
            (
                "http://",
                "https://",
            ),
        ):
            target = f"https://{target}"

        return target
