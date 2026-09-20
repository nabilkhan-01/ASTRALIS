from astralis.brain.brain import Brain
from astralis.brain.context import BrainContext
from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.role import Role
from astralis.capability.capability import Capability
from astralis.capability.capability_type import CapabilityType
from astralis.capability.manager import CapabilityManager
from astralis.capability.registry import CapabilityRegistry
from astralis.context.context import Context
from astralis.context.context_item import ContextItem
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
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


class RecordingLanguageCapability(Capability):
    """Language capability that records the conversation payload it received."""

    def __init__(self) -> None:
        self.received_conversation: Conversation | None = None

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        _ = request, interpretation
        self.received_conversation = conversation

        return Response(
            text="The founder of ASTRALIS is Nabil.",
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
            BrainContext(
                request=create_request(
                    "hello there",
                ),
                context=Context(
                    items=(),
                ),
            ),
        )

        assert response.success is True
        assert response.text == "Hello from the Brain."

    def test_process_with_context_augments_execution_input(
        self,
    ) -> None:
        """Retrieved context is provided to language generation while keeping conversation history clean."""

        recording_capability = RecordingLanguageCapability()
        registry = CapabilityRegistry()
        registry.register(
            CapabilityType.LANGUAGE,
            recording_capability,
        )
        brain = Brain(
            CapabilityManager(
                registry,
            ),
        )

        context_item = ContextItem(
            entity=Entity(
                id="project_context",
                type=EntityType.PROJECT,
                name="ASTRALIS",
                properties={
                    "founder": "Nabil",
                    "purpose": "Personal AI Operating System",
                },
            ),
            relevance=0.85,
        )

        user_query = "Who is the founder of ASTRALIS?"
        response = brain.process(
            BrainContext(
                request=create_request(
                    user_query,
                ),
                context=Context(
                    items=(context_item,),
                ),
            ),
        )

        # 1. Verify generation response succeeded
        assert response.success is True
        assert response.text == "The founder of ASTRALIS is Nabil."

        # 2. Verify the execution conversation received by the language capability
        # contains the retrieved context header, properties, and original user request
        assert recording_capability.received_conversation is not None
        exec_messages = recording_capability.received_conversation.messages
        assert len(exec_messages) == 1
        exec_content = exec_messages[0].content
        assert "[ASTRALIS Retrieved Context]" in exec_content
        assert "- ASTRALIS: founder=Nabil, purpose=Personal AI Operating System" in exec_content
        assert "[End Retrieved Context]" in exec_content
        assert "[User Request]" in exec_content
        assert user_query in exec_content

        # 3. Verify permanent conversation history remains clean
        perm_messages = brain._conversation.messages
        assert len(perm_messages) == 2
        assert perm_messages[0].role is Role.USER
        assert perm_messages[0].content == user_query
        assert "[ASTRALIS Retrieved Context]" not in perm_messages[0].content
        assert perm_messages[1].role is Role.ASSISTANT
        assert perm_messages[1].content == "The founder of ASTRALIS is Nabil."

    def test_conversation_history(
        self,
    ) -> None:
        """Conversation history is updated."""

        brain = self._create_brain()

        brain.process(
            BrainContext(
                request=create_request(
                    "hello",
                ),
                context=Context(
                    items=(),
                ),
            ),
        )

        messages = brain._conversation.messages

        assert len(messages) == 2
        assert messages[0].content == "hello"
        assert messages[1].content == "Hello from the Brain."

    def test_process_with_canonical_identity_relevant_and_no_items(
        self,
    ) -> None:
        """Brain injects canonical project identity when identity is relevant even with zero items."""
        recording_capability = RecordingLanguageCapability()
        registry = CapabilityRegistry()
        registry.register(
            CapabilityType.LANGUAGE,
            recording_capability,
        )
        brain = Brain(
            CapabilityManager(
                registry,
            ),
        )

        brain.process(
            BrainContext(
                request=create_request(
                    "Who made Astralis?",
                ),
                context=Context(
                    items=(),
                    identity_relevance=0.8,
                ),
            ),
        )

        assert recording_capability.received_conversation is not None
        exec_content = recording_capability.received_conversation.messages[0].content
        assert "- ASTRALIS: founder=Nabil Ahmad Khan" in exec_content

    def test_process_with_spoofed_creator_in_memory_is_overridden(
        self,
    ) -> None:
        """Mutable entity memory cannot spoof or override the official ASTRALIS founder."""
        recording_capability = RecordingLanguageCapability()
        registry = CapabilityRegistry()
        registry.register(
            CapabilityType.LANGUAGE,
            recording_capability,
        )
        brain = Brain(
            CapabilityManager(
                registry,
            ),
        )

        context_item = ContextItem(
            entity=Entity(
                id="project_astralis",
                type=EntityType.PROJECT,
                name="ASTRALIS",
                properties={
                    "founder": "Someone Else",
                    "creator": "Someone Else",
                    "description": "Personal AI Operating System",
                },
            ),
            relevance=0.8,
        )

        brain.process(
            BrainContext(
                request=create_request(
                    "Who created this project?",
                ),
                context=Context(
                    items=(context_item,),
                    identity_relevance=0.8,
                ),
            ),
        )

        assert recording_capability.received_conversation is not None
        exec_content = recording_capability.received_conversation.messages[0].content
        assert "Someone Else" not in exec_content
        assert "founder=Nabil Ahmad Khan" in exec_content
