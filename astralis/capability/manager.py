from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.plan import ExecutionPlan
from astralis.brain.response import Response
from astralis.capability.registry import CapabilityRegistry


class CapabilityManager:
    """Coordinates capability execution."""

    def __init__(
        self,
        registry: CapabilityRegistry,
    ) -> None:
        self.registry = registry

    def execute(
        self,
        conversation: Conversation,
        interpretation: Interpretation,
        plan: ExecutionPlan,
    ) -> Response:
        capability = self.registry.get(
            plan.capability,
        )

        return capability.execute(
            conversation,
            interpretation,
        )