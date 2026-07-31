import pytest

from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.capability.capability_type import CapabilityType
from astralis.capability.registry import CapabilityRegistry


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


class TestCapabilityRegistry:
    """Tests for the CapabilityRegistry."""

    @staticmethod
    def _create_registry() -> CapabilityRegistry:
        """Create a fresh capability registry."""

        return CapabilityRegistry()

    def test_register_and_get(
        self,
    ) -> None:
        """Register and retrieve a capability."""

        registry = self._create_registry()

        capability = DummyCapability()

        registry.register(
            CapabilityType.LANGUAGE,
            capability,
        )

        assert (
            registry.get(
                CapabilityType.LANGUAGE,
            )
            is capability
        )

    def test_duplicate_registration(
        self,
    ) -> None:
        """Registering the same capability twice raises an error."""

        registry = self._create_registry()

        registry.register(
            CapabilityType.LANGUAGE,
            DummyCapability(),
        )

        with pytest.raises(
            ValueError,
        ):
            registry.register(
                CapabilityType.LANGUAGE,
                DummyCapability(),
            )

    def test_missing_capability(
        self,
    ) -> None:
        """Requesting an unknown capability raises an error."""

        registry = self._create_registry()

        with pytest.raises(
            ValueError,
        ):
            registry.get(
                CapabilityType.LANGUAGE,
            )

    def test_contains(
        self,
    ) -> None:
        """Check whether a capability is registered."""

        registry = self._create_registry()

        assert CapabilityType.LANGUAGE not in registry

        registry.register(
            CapabilityType.LANGUAGE,
            DummyCapability(),
        )

        assert CapabilityType.LANGUAGE in registry
