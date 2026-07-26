from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.memory.alarm import AlarmMemory


class AlarmCapability(Capability):
    """Manages user alarms."""

    def __init__(
        self,
        alarms: AlarmMemory,
    ) -> None:
        self.alarms = alarms

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Execute an alarm command."""

        _ = conversation, interpretation

        text = request.text.strip()

        if text.lower().startswith(
            "alarm ",
        ):
            return self._handle_add_alarm(
                text,
            )

        if text.lower() == "alarms":
            return self._handle_list_alarms()

        if text.lower().startswith(
            "enable alarm",
        ):
            return self._handle_enable_alarm(
                text,
            )

        if text.lower().startswith(
            "disable alarm",
        ):
            return self._handle_disable_alarm(
                text,
            )

        if text.lower().startswith(
            "delete alarm",
        ):
            return self._handle_delete_alarm(
                text,
            )

        return Response(
            text="Unknown alarm command.",
            success=False,
        )

    def _handle_add_alarm(
        self,
        text: str,
    ) -> Response:
        """Add an alarm."""

        parts = text.split()

        if len(parts) < 3:
            return Response(
                text="Usage: alarm <time> <title>",
                success=False,
            )

        time = parts[1]

        if not self._is_valid_time(
            time,
        ):
            return Response(
                text="Invalid time. Use HH:MM.",
                success=False,
            )

        title = " ".join(
            parts[2:],
        )

        alarm_id = self.alarms.add_alarm(
            title=title,
            time=time,
        )

        return Response(
            text=f"Alarm {alarm_id} added.",
            success=True,
        )

    def _handle_list_alarms(
        self,
    ) -> Response:
        """List all alarms."""

        alarms = self.alarms.get_alarms()

        if not alarms:
            return Response(
                text="No alarms found.",
                success=True,
            )

        lines = []

        for alarm in alarms:
            status = "Enabled" if alarm.enabled else "Disabled"

            lines.append(f"{alarm.id}. {alarm.title} | {alarm.time} | {status}")

        return Response(
            text="\n".join(
                lines,
            ),
            success=True,
        )

    def _handle_enable_alarm(
        self,
        text: str,
    ) -> Response:
        """Enable an alarm."""

        parts = text.split()

        if len(parts) != 3:
            return Response(
                text="Please specify the alarm number.",
                success=False,
            )

        alarm_id = int(
            parts[2],
        )

        enabled = self.alarms.enable_alarm(
            alarm_id,
        )

        if not enabled:
            return Response(
                text="Alarm not found.",
                success=False,
            )

        return Response(
            text="Alarm enabled.",
            success=True,
        )

    def _handle_disable_alarm(
        self,
        text: str,
    ) -> Response:
        """Disable an alarm."""

        parts = text.split()

        if len(parts) != 3:
            return Response(
                text="Please specify the alarm number.",
                success=False,
            )

        alarm_id = int(
            parts[2],
        )

        disabled = self.alarms.disable_alarm(
            alarm_id,
        )

        if not disabled:
            return Response(
                text="Alarm not found.",
                success=False,
            )

        return Response(
            text="Alarm disabled.",
            success=True,
        )

    def _handle_delete_alarm(
        self,
        text: str,
    ) -> Response:
        """Delete an alarm."""

        parts = text.split()

        if len(parts) != 3:
            return Response(
                text="Please specify the alarm number.",
                success=False,
            )

        alarm_id = int(
            parts[2],
        )

        deleted = self.alarms.delete_alarm(
            alarm_id,
        )

        if not deleted:
            return Response(
                text="Alarm not found.",
                success=False,
            )

        return Response(
            text="Alarm deleted.",
            success=True,
        )

    def _is_valid_time(
        self,
        time: str,
    ) -> bool:
        """Validate a 24-hour time."""

        parts = time.split(
            ":",
        )

        if len(parts) != 2:
            return False

        hour, minute = parts

        if not (hour.isdigit() and minute.isdigit()):
            return False

        hour_value = int(
            hour,
        )

        minute_value = int(
            minute,
        )

        return 0 <= hour_value <= 23 and 0 <= minute_value <= 59
