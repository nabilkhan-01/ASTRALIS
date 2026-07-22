from datetime import datetime

from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability


class TimeCapability(Capability):
    """Provides the current local date and time."""

    def __init__(self) -> None:
        self._clock = datetime.now

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Return the current date and/or time."""

        _ = request, conversation

        now = self._clock()

        if "time" in interpretation.entities:
            return Response(
                text=f"The current time is {now.strftime('%I:%M %p')}.",
                success=True,
            )

        if "date" in interpretation.entities:
            return Response(
                text=f"Today is {now.strftime('%A, %d %B %Y')}.",
                success=True,
            )

        return Response(
            text=(
                f"Today is {now.strftime('%A, %d %B %Y')} "
                f"and the current time is {now.strftime('%I:%M %p')}."
            ),
            success=True,
        )