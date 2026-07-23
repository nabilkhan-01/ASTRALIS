from astralis.brain.execution_plan import ExecutionPlan
from astralis.brain.interpretation import Interpretation
from astralis.capability.capability_type import CapabilityType


class Planner:
    """Creates execution plans from interpreted requests."""

    def plan(
        self,
        interpretation: Interpretation,
    ) -> ExecutionPlan:
        """Create an execution plan."""

        return ExecutionPlan(
            capability=self._select_capability(
                interpretation,
            ),
        )

    def _select_capability(
        self,
        interpretation: Interpretation,
    ) -> CapabilityType:
        """Select the capability required for the request."""

        if "memory" in interpretation.entities:
            return CapabilityType.LANGUAGE

        if (
            "time" in interpretation.entities
            or "date" in interpretation.entities
        ):
            return CapabilityType.TIME

        if "calculator" in interpretation.entities:
            return CapabilityType.CALCULATOR

        if "search" in interpretation.entities:
            return CapabilityType.SEARCH
        
        if "weather" in interpretation.entities:
            return CapabilityType.WEATHER

        
        return CapabilityType.LANGUAGE