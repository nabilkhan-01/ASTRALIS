from astralis.api.email import EmailApi
from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability


class EmailCapability(Capability):
    """Manages email operations."""

    def __init__(
        self,
    ) -> None:
        self.email = EmailApi()

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Execute an email command."""

        _ = conversation, interpretation

        text = request.text.strip()

        if text.lower() == "email":
            return self._handle_help()

        if text.lower().startswith(
            "draft email",
        ):
            return self._handle_draft(
                text,
            )

        if text.lower().startswith(
            "send email",
        ):
            return self._handle_send(
                text,
            )

        return Response(
            text="Unknown email command.",
            success=False,
        )

    def _handle_help(
        self,
    ) -> Response:
        """Display email commands."""

        return Response(
            text=(
                "Available commands:\n"
                "draft email <recipient> <subject>\n"
                "send email <recipient> <subject>"
            ),
            success=True,
        )

    def _handle_draft(
        self,
        text: str,
    ) -> Response:
        """Create an email draft."""

        parts = text.split(
            maxsplit=3,
        )

        if len(parts) != 4:
            return Response(
                text=("Usage: draft email <recipient> <subject>"),
                success=False,
            )

        recipient = parts[2]
        subject = parts[3]

        message = self.email.create_draft(
            recipient=recipient,
            subject=subject,
            body="",
        )

        return Response(
            text=message,
            success=True,
        )

    def _handle_send(
        self,
        text: str,
    ) -> Response:
        """Attempt to send an email."""

        _ = text

        return Response(
            text="Sending emails is not yet supported.",
            success=False,
        )
