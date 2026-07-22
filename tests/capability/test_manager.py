from astralis.brain.execution_plan import ExecutionPlan
from astralis.brain.interpretation import Interpretation
from astralis.brain.intent import Intent
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.capability.capability_type import CapabilityType
from astralis.capability.manager import CapabilityManager
from astralis.capability.registry import CapabilityRegistry

from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.request_factory import (
    create_request,
)


class DummyCapability(Capability):
    """Dummy capability used for testing."""

    def execute(
        self,
        request,
        conversation,
        interpretation,
    ) -> Response:
        return Response(
            text="Dummy response.",
            success=True,
        )


class TestCapabilityManager:
    """Tests for the CapabilityManager."""

    def setup_method(self) -> None:
        """Create a capability manager."""

        registry = CapabilityRegistry()

        registry.register(
            CapabilityType.LANGUAGE,
            DummyCapability(),
        )

        self.manager = CapabilityManager(
            registry,
        )

    def test_execute(self) -> None:
        """Execute a registered capability."""

        response = self.manager.execute(
            request=create_request("hello"),
            conversation=create_conversation(),
            interpretation=Interpretation(
                intent=Intent.CONVERSATION,
                entities=[],
            ),
            plan=ExecutionPlan(
                capability=CapabilityType.LANGUAGE,
            ),
        )

        assert response.success is True
        assert response.text == "Dummy response."