from astralis.brain.brain import Brain
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.capability.capability_type import CapabilityType
from astralis.capability.manager import CapabilityManager
from astralis.capability.registry import CapabilityRegistry
from tests.helpers.request_factory import (
    create_request,
)


class DummyLanguageCapability(Capability):
    """Dummy language capability."""

    def execute(
        self,
        request,
        conversation,
        interpretation,
    ) -> Response:
        return Response(
            text="Hello from the Brain.",
            success=True,
        )


class TestBrain:
    """Integration tests for the Brain."""

    def setup_method(self) -> None:
        """Create a Brain."""

        registry = CapabilityRegistry()

        registry.register(
            CapabilityType.LANGUAGE,
            DummyLanguageCapability(),
        )

        manager = CapabilityManager(
            registry,
        )

        self.brain = Brain(
            manager,
        )

    def test_process(self) -> None:
        """Process a normal conversation."""

        response = self.brain.process(
            create_request(
                "hello there",
            ),
        )

        assert response.success is True
        assert response.text == "Hello from the Brain."

    def test_conversation_history(self) -> None:
        """Conversation history is updated."""

        self.brain.process(
            create_request(
                "hello",
            ),
        )

        messages = self.brain.conversation.messages

        assert len(messages) == 2

        assert messages[0].content == "hello"

        assert messages[1].content == "Hello from the Brain."
