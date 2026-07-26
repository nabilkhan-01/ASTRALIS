from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.plan import Plan
from astralis.brain.request import Request
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
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
        plan: Plan,
    ) -> Response:
        capability = self.registry.get(
            plan.capability,
        )

        return capability.execute(
            request,
            conversation,
            interpretation,
        )
