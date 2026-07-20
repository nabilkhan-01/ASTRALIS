from astralis.brain.interpretation import Interpretation
from astralis.brain.execution_plan import ExecutionPlan
from astralis.capability.capability_type import CapabilityType


class Planner:
    """Creates execution plans for interpreted requests."""

    def plan(
        self,
        interpretation: Interpretation,
    ) -> ExecutionPlan:
        """Create an execution plan."""

        return ExecutionPlan(
            capability=CapabilityType.LANGUAGE,
        )