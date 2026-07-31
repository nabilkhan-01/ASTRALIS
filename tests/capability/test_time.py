from datetime import UTC, datetime

from astralis.capability.time import TimeCapability
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestTimeCapability:
    """Tests for the TimeCapability."""

    @staticmethod
    def _create_capability() -> TimeCapability:
        """Create a time capability with a fixed clock."""

        capability = TimeCapability()

        capability._clock = lambda: datetime(
            2026,
            7,
            23,
            10,
            30,
            tzinfo=UTC,
        )

        return capability

    def test_time(
        self,
    ) -> None:
        """Return the current time."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "time",
            ),
            create_conversation(),
            create_interpretation(
                entities=["time"],
            ),
        )

        assert response.success is True
        assert response.text == "The current time is 10:30 AM."

    def test_date(
        self,
    ) -> None:
        """Return the current date."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "date",
            ),
            create_conversation(),
            create_interpretation(
                entities=["date"],
            ),
        )

        assert response.success is True
        assert response.text == "Today is Thursday, 23 July 2026."

    def test_date_and_time(
        self,
    ) -> None:
        """Return both the current date and time."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "today",
            ),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success is True
        assert (
            response.text == "Today is Thursday, 23 July 2026 "
            "and the current time is 10:30 AM."
        )
