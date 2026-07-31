from typing import ClassVar

from astralis.brain.interpretation import Interpretation
from astralis.brain.plan import Plan
from astralis.capability.capability_type import CapabilityType


class Planner:
    """Creates execution plans from interpreted requests."""

    CAPABILITY_MAP: ClassVar[dict[str, CapabilityType]] = {
        "time": CapabilityType.TIME,
        "date": CapabilityType.TIME,
        "calculator": CapabilityType.CALCULATOR,
        "weather": CapabilityType.WEATHER,
        "search": CapabilityType.SEARCH,
        "notes": CapabilityType.NOTES,
        "alarm": CapabilityType.ALARM,
        "calendar": CapabilityType.CALENDAR,
        "email": CapabilityType.EMAIL,
        "browser": CapabilityType.BROWSER,
        "memory": CapabilityType.LANGUAGE,
        "file_system": CapabilityType.FILE_SYSTEM,
    }

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

        for entity in interpretation.entities:
            capability = self.CAPABILITY_MAP.get(
                entity,
            )

            if capability is not None:
                return capability

        return CapabilityType.LANGUAGE
