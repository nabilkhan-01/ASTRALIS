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

    def setup_method(self) -> None:
        self.capability = TimeCapability()

        self.capability._clock = lambda: datetime(
            2026,
            7,
            23,
            10,
            30,
            tzinfo=UTC,
        )

        self.conversation = create_conversation()

    def test_time(self) -> None:
        """Returns the current time."""

        response = self.capability.execute(
            create_request("time"),
            self.conversation,
            create_interpretation(
                entities=["time"],
            ),
        )

        assert response.success is True
        assert response.text == "The current time is 10:30 AM."

    def test_date(self) -> None:
        """Returns the current date."""

        response = self.capability.execute(
            create_request("date"),
            self.conversation,
            create_interpretation(
                entities=["date"],
            ),
        )

        assert response.success is True
        assert response.text == "Today is Thursday, 23 July 2026."

    def test_date_and_time(self) -> None:
        """Returns both date and time."""

        response = self.capability.execute(
            create_request("today"),
            self.conversation,
            create_interpretation(),
        )

        assert response.success is True
        assert (
            response.text
            == "Today is Thursday, 23 July 2026 and the current time is 10:30 AM."
        )
