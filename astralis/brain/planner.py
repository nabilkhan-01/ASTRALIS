from astralis.brain.interpretation import Interpretation
from astralis.brain.plan import Plan
from astralis.capability.capability_type import CapabilityType


class Planner:
    """Creates execution plans from interpreted requests."""

    def plan(
        self,
        interpretation: Interpretation,
    ) -> Plan:
        """Create an execution plan."""

        return Plan(
            capability=self._select_capability(
                interpretation,
            ),
        )

    def _select_capability(
        self,
        interpretation: Interpretation,
    ) -> CapabilityType:
        """Select the capability required for the request."""

        if "time" in interpretation.entities or "date" in interpretation.entities:
            return CapabilityType.TIME

        if "calculator" in interpretation.entities:
            return CapabilityType.CALCULATOR

        if "weather" in interpretation.entities:
            return CapabilityType.WEATHER

        if "search" in interpretation.entities:
            return CapabilityType.SEARCH

        if "notes" in interpretation.entities:
            return CapabilityType.NOTES

        if "alarm" in interpretation.entities:
            return CapabilityType.ALARM

        if "calendar" in interpretation.entities:
            return CapabilityType.CALENDAR

        if "email" in interpretation.entities:
            return CapabilityType.EMAIL

        if "browser" in interpretation.entities:
            return CapabilityType.BROWSER

        if "memory" in interpretation.entities:
            return CapabilityType.LANGUAGE

        if "file_system" in interpretation.entities:
            return CapabilityType.FILE_SYSTEM

        return CapabilityType.LANGUAGE
