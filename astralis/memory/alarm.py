import json
from dataclasses import asdict
from pathlib import Path

from astralis.models.alarm import Alarm


class AlarmMemory:
    """Stores and retrieves user alarms."""

    DATA_FILE = Path(
        "data/alarms.json",
    )

    def __init__(
        self,
    ) -> None:
        self.DATA_FILE.parent.mkdir(
            exist_ok=True,
        )

        if not self.DATA_FILE.exists():
            self.DATA_FILE.write_text(
                "[]",
                encoding="utf-8",
            )

    def add_alarm(
        self,
        title: str,
        time: str,
    ) -> int:
        """Add an alarm."""

        alarms = self._load()

        alarm = Alarm(
            id=len(alarms) + 1,
            title=title,
            time=time,
        )

        alarms.append(
            alarm,
        )

        self._save(
            alarms,
        )

        return alarm.id

    def get_alarms(
        self,
    ) -> list[Alarm]:
        """Return all alarms."""

        return self._load()

    def delete_alarm(
        self,
        alarm_id: int,
    ) -> bool:
        """Delete an alarm."""

        alarms = self._load()

        new_alarms = [
            alarm
            for alarm in alarms
            if alarm.id != alarm_id
        ]

        if len(new_alarms) == len(alarms):
            return False

        renumbered = [
            Alarm(
                id=index,
                title=alarm.title,
                time=alarm.time,
                enabled=alarm.enabled,
            )
            for index, alarm in enumerate(
                new_alarms,
                start=1,
            )
        ]

        self._save(
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

        alarms = self._load()

        updated = []

        found = False

        for alarm in alarms:
            if alarm.id == alarm_id:
                updated.append(
                    Alarm(
                        id=alarm.id,
                        title=alarm.title,
                        time=alarm.time,
                        enabled=enabled,
                    )
                )

                found = True

            else:
                updated.append(
                    alarm,
                )

        if not found:
            return False

        self._save(
            updated,
        )

        return True

    def _load(
        self,
    ) -> list[Alarm]:
        """Load alarms."""

        with open(
            self.DATA_FILE,
            encoding="utf-8",
        ) as file:
            data = json.load(
                file,
            )

        return [
            Alarm(
                **alarm,
            )
            for alarm in data
        ]

    def _save(
        self,
        alarms: list[Alarm],
    ) -> None:
        """Save alarms."""

        with open(
            self.DATA_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                [
                    asdict(
                        alarm,
                    )
                    for alarm in alarms
                ],
                file,
                indent=4,
            )