from astralis.capability.alarm import AlarmCapability

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

    def setup_method(
        self,
    ) -> None:
        self.capability = AlarmCapability()

        self.capability.alarms._save(
            [],
        )

    def test_add_alarm(
        self,
    ) -> None:
        response = self.capability.execute(
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
        self.capability.alarms.add_alarm(
            "Wake up",
            "07:00",
        )

        response = self.capability.execute(
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
        self.capability.alarms.add_alarm(
            "Wake up",
            "07:00",
        )

        self.capability.alarms.disable_alarm(
            1,
        )

        response = self.capability.execute(
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
        self.capability.alarms.add_alarm(
            "Wake up",
            "07:00",
        )

        response = self.capability.execute(
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
        self.capability.alarms.add_alarm(
            "Wake up",
            "07:00",
        )

        response = self.capability.execute(
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
        response = self.capability.execute(
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
        response = self.capability.execute(
            create_request(
                "alarm 25:99 Wake up",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is False
        assert response.text == "Invalid time. Use HH:MM."

    def test_missing_alarm_number(
        self,
    ) -> None:
        response = self.capability.execute(
            create_request(
                "delete alarm",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is False

    def test_alarm_not_found(
        self,
    ) -> None:
        response = self.capability.execute(
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
        response = self.capability.execute(
            create_request(
                "alarm delete everything",
            ),
            create_conversation(),
            create_interpretation(
                entities=["alarm"],
            ),
        )

        assert response.success is False