from dataclasses import replace
from pathlib import Path

from astralis.memory.base import BaseMemory
from astralis.models.alarm import Alarm
from astralis.storage.json import JsonStorage


class AlarmMemory(BaseMemory[Alarm]):
    """Stores and retrieves user alarms."""

    MODEL = Alarm

    DATA_FILE = Path(
        "data/alarms.json",
    )

    def __init__(
        self,
    ) -> None:
        super().__init__(
            JsonStorage(
                self.DATA_FILE,
            ),
        )

    def add_alarm(
        self,
        title: str,
        time: str,
    ) -> int:
        """Add an alarm."""

        alarms = self._load_models()

        alarm = Alarm(
            id=len(alarms) + 1,
            title=title,
            time=time,
        )

        alarms.append(
            alarm,
        )

        self._save_models(
            alarms,
        )

        return alarm.id

    def get_alarms(
        self,
    ) -> list[Alarm]:
        """Return all alarms."""

        return self._load_models()

    def clear(
        self,
    ) -> None:
        """Remove all stored alarms."""

        self._save_models(
            [],
        )

    def delete_alarm(
        self,
        alarm_id: int,
    ) -> bool:
        """Delete an alarm."""

        alarms = self._load_models()

        new_alarms = [alarm for alarm in alarms if alarm.id != alarm_id]

        if len(new_alarms) == len(alarms):
            return False

        renumbered = [
            replace(
                alarm,
                id=index,
            )
            for index, alarm in enumerate(
                new_alarms,
                start=1,
            )
        ]

        self._save_models(
            renumbered,
        )

        return True

    def enable_alarm(
        self,
        alarm_id: int,
    ) -> bool:
        """Enable an alarm."""

        return self._set_enabled(
            alarm_id,
            True,
        )

    def disable_alarm(
        self,
        alarm_id: int,
    ) -> bool:
        """Disable an alarm."""

        return self._set_enabled(
            alarm_id,
            False,
        )

    def _set_enabled(
        self,
        alarm_id: int,
        enabled: bool,
    ) -> bool:
        """Enable or disable an alarm."""

        alarms = self._load_models()

        updated_alarms = []

        found = False

        for alarm in alarms:
            if alarm.id == alarm_id:
                updated_alarms.append(
                    replace(
                        alarm,
                        enabled=enabled,
                    ),
                )

                found = True

            else:
                updated_alarms.append(
                    alarm,
                )

        if not found:
            return False

        self._save_models(
            updated_alarms,
        )

        return True
