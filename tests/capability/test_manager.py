from astralis.brain.conversation import Conversation
from astralis.brain.intent import Intent
from astralis.brain.interpretation import Interpretation
from astralis.brain.plan import Plan
from astralis.brain.request import Request
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
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Execute the dummy capability."""

        _ = request, conversation, interpretation

        return Response(
            text="Dummy response.",
        )


class TestCapabilityManager:
    """Tests for the CapabilityManager."""

    @staticmethod
    def _create_manager() -> CapabilityManager:
        """Create a capability manager."""

        registry = CapabilityRegistry()

        registry.register(
            CapabilityType.LANGUAGE,
            DummyCapability(),
        )

        return CapabilityManager(
            registry,
        )

    def test_execute(
        self,
    ) -> None:
        """Execute a registered capability."""

        manager = self._create_manager()

        response = manager.execute(
            request=create_request(
                "hello",
            ),
            conversation=create_conversation(),
            interpretation=Interpretation(
                intent=Intent.CONVERSATION,
                entities=[],
            ),
            plan=Plan(
                capability=CapabilityType.LANGUAGE,
            ),
        )

        assert response.success is True
        assert response.text == "Dummy response."
