from astralis.brain.brain import Brain
from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
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
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        _ = request, conversation, interpretation

        return Response(
            text="Hello from the Brain.",
        )


class TestBrain:
    """Integration tests for the Brain."""

    @staticmethod
    def _create_brain() -> Brain:
        """Create a Brain for testing."""

        registry = CapabilityRegistry()

        registry.register(
            CapabilityType.LANGUAGE,
            DummyLanguageCapability(),
        )

        manager = CapabilityManager(
            registry,
        )

        return Brain(
            manager,
        )

    def test_process(
        self,
    ) -> None:
        """Process a normal conversation."""

        brain = self._create_brain()

        response = brain.process(
            create_request(
                "hello there",
            ),
        )

        assert response.success is True
        assert response.text == "Hello from the Brain."

    def test_conversation_history(
        self,
    ) -> None:
        """Conversation history is updated."""

        brain = self._create_brain()

        brain.process(
            create_request(
                "hello",
            ),
        )

        messages = brain.conversation.messages

        assert len(messages) == 2
        assert messages[0].content == "hello"
        assert messages[1].content == "Hello from the Brain."
