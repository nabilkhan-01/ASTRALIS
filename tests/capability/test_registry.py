import pytest

from astralis.capability.capability import Capability
from astralis.capability.capability_type import CapabilityType
from astralis.capability.registry import CapabilityRegistry


class DummyCapability(Capability):
    """Dummy capability used for testing."""

    def execute(
        self,
        request,
        conversation,
        interpretation,
    ):
        return None


class TestCapabilityRegistry:
    """Tests for the CapabilityRegistry."""

    def setup_method(self) -> None:
        """Create a fresh registry."""

        self.registry = CapabilityRegistry()

    def test_register_and_get(self) -> None:
        """Register and retrieve a capability."""

        capability = DummyCapability()

        self.registry.register(
            CapabilityType.LANGUAGE,
            capability,
        )

        assert (
            self.registry.get(
                CapabilityType.LANGUAGE,
            )
            is capability
        )

    def test_duplicate_registration(self) -> None:
        """Registering the same capability twice raises an error."""

        capability = DummyCapability()

        self.registry.register(
            CapabilityType.LANGUAGE,
            capability,
        )

        with pytest.raises(ValueError):
            self.registry.register(
                CapabilityType.LANGUAGE,
                DummyCapability(),
            )

    def test_missing_capability(self) -> None:
        """Requesting an unknown capability raises an error."""

        with pytest.raises(ValueError):
            self.registry.get(
                CapabilityType.LANGUAGE,
            )