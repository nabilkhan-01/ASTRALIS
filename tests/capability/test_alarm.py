from astralis.capability.alarm import AlarmCapability
from astralis.memory.alarm import AlarmMemory
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestAlarmCapability:
    """Tests for AlarmCapability."""

    @staticmethod
    def _create_capability() -> AlarmCapability:
        """Create a clean alarm capability."""

        alarms = AlarmMemory()
        alarms.clear()

        return AlarmCapability(
            alarms,
        )

    def test_add_alarm(
        self,
    ) -> None:
        """Add an alarm."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "alarm 07:00 Wake up",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is True
        assert response.text == "Alarm 1 added."

    def test_list_alarms(
        self,
    ) -> None:
        """List alarms."""

        capability = self._create_capability()

        capability.alarms.add_alarm(
            "Wake up",
            "07:00",
        )

        response = capability.execute(
            create_request(
                "alarms",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is True
        assert "Wake up" in response.text
        assert "Enabled" in response.text

    def test_enable_alarm(
        self,
    ) -> None:
        """Enable an alarm."""

        capability = self._create_capability()

        capability.alarms.add_alarm(
            "Wake up",
            "07:00",
        )

        capability.alarms.disable_alarm(
            1,
        )

        response = capability.execute(
            create_request(
                "enable alarm 1",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is True
        assert response.text == "Alarm enabled."

    def test_disable_alarm(
        self,
    ) -> None:
        """Disable an alarm."""

        capability = self._create_capability()

        capability.alarms.add_alarm(
            "Wake up",
            "07:00",
        )

        response = capability.execute(
            create_request(
                "disable alarm 1",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is True
        assert response.text == "Alarm disabled."

    def test_delete_alarm(
        self,
    ) -> None:
        """Delete an alarm."""

        capability = self._create_capability()

        capability.alarms.add_alarm(
            "Wake up",
            "07:00",
        )

        response = capability.execute(
            create_request(
                "delete alarm 1",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is True
        assert response.text == "Alarm deleted."

    def test_empty_alarms(
        self,
    ) -> None:
        """List alarms when none exist."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "alarms",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is True
        assert response.text == "No alarms found."

    def test_invalid_time(
        self,
    ) -> None:
        """Reject an invalid time."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "alarm 25:99 Wake up",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is False
        assert (
            response.text
            == "Invalid time. Use HH:MM (24-hour format)."
        )

    def test_missing_alarm_number(
        self,
    ) -> None:
        """Reject a missing alarm number."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "delete alarm",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is False
        assert response.text == "Usage: delete alarm <id>"

    def test_alarm_not_found(
        self,
    ) -> None:
        """Reject an unknown alarm."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "enable alarm 5",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is False
        assert response.text == "Alarm not found."

    def test_unknown_command(
        self,
    ) -> None:
        """Reject an unknown alarm command."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "alarm delete everything",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is False
        assert (
            response.text
            == "Invalid time. Use HH:MM (24-hour format)."
        )
