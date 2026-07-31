from astralis.memory.alarm import AlarmMemory


class TestAlarmMemory:
    """Tests for AlarmMemory."""

    @staticmethod
    def _create_memory() -> AlarmMemory:
        """Create an empty alarm memory."""

        memory = AlarmMemory()
        memory.clear()

        return memory

    def test_add_alarm(
        self,
    ) -> None:
        """Add an alarm."""

        memory = self._create_memory()

        alarm_id = memory.add_alarm(
            "Wake up",
            "07:00",
        )

        assert alarm_id == 1

    def test_get_alarms(
        self,
    ) -> None:
        """Return all alarms."""

        memory = self._create_memory()

        memory.add_alarm(
            "Wake up",
            "07:00",
        )

        memory.add_alarm(
            "Gym",
            "18:00",
        )

        alarms = memory.get_alarms()

        assert len(alarms) == 2

        assert alarms[0].id == 1
        assert alarms[0].title == "Wake up"
        assert alarms[0].time == "07:00"
        assert alarms[0].enabled is True

        assert alarms[1].id == 2
        assert alarms[1].title == "Gym"
        assert alarms[1].time == "18:00"
        assert alarms[1].enabled is True

    def test_delete_alarm(
        self,
    ) -> None:
        """Delete an alarm."""

        memory = self._create_memory()

        memory.add_alarm(
            "Wake up",
            "07:00",
        )

        assert (
            memory.delete_alarm(
                1,
            )
            is True
        )

        assert memory.get_alarms() == []

    def test_alarm_ids_are_renumbered(
        self,
    ) -> None:
        """Renumber alarm IDs after deletion."""

        memory = self._create_memory()

        memory.add_alarm(
            "Wake up",
            "07:00",
        )

        memory.add_alarm(
            "Gym",
            "18:00",
        )

        memory.add_alarm(
            "Study",
            "21:00",
        )

        memory.delete_alarm(
            2,
        )

        alarms = memory.get_alarms()

        assert len(alarms) == 2

        assert alarms[0].id == 1
        assert alarms[0].title == "Wake up"

        assert alarms[1].id == 2
        assert alarms[1].title == "Study"

    def test_enable_alarm(
        self,
    ) -> None:
        """Enable an alarm."""

        memory = self._create_memory()

        memory.add_alarm(
            "Wake up",
            "07:00",
        )

        memory.disable_alarm(
            1,
        )

        assert (
            memory.enable_alarm(
                1,
            )
            is True
        )

        alarms = memory.get_alarms()

        assert alarms[0].enabled is True

    def test_disable_alarm(
        self,
    ) -> None:
        """Disable an alarm."""

        memory = self._create_memory()

        memory.add_alarm(
            "Wake up",
            "07:00",
        )

        assert (
            memory.disable_alarm(
                1,
            )
            is True
        )

        alarms = memory.get_alarms()

        assert alarms[0].enabled is False

    def test_delete_missing_alarm(
        self,
    ) -> None:
        """Deleting a missing alarm returns False."""

        memory = self._create_memory()

        assert (
            memory.delete_alarm(
                999,
            )
            is False
        )

    def test_enable_missing_alarm(
        self,
    ) -> None:
        """Enabling a missing alarm returns False."""

        memory = self._create_memory()

        assert (
            memory.enable_alarm(
                999,
            )
            is False
        )

    def test_disable_missing_alarm(
        self,
    ) -> None:
        """Disabling a missing alarm returns False."""

        memory = self._create_memory()

        assert (
            memory.disable_alarm(
                999,
            )
            is False
        )

    def test_empty_alarms(
        self,
    ) -> None:
        """Return an empty alarm list."""

        memory = self._create_memory()

        assert memory.get_alarms() == []
