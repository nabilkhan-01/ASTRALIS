from astralis.capability.capability import Capability
from astralis.capability.capability_type import CapabilityType


class CapabilityRegistry:
    """Stores all registered capabilities."""

    def __init__(self) -> None:
        self._capabilities: dict[
            CapabilityType,
            Capability,
        ] = {}

    def register(
        self,
        capability_type: CapabilityType,
        capability: Capability,
    ) -> None:
        """Register a capability."""

        self._capabilities[
            capability_type
        ] = capability

    def get(
        self,
        capability_type: CapabilityType,
    ) -> Capability:
        """Return a registered capability."""

        capability = self._capabilities.get(
            capability_type,
        )

        if capability is None:
            raise ValueError(
                f"No capability registered for '{capability_type}'",
            )
        
        
        return self._capabilities[
            capability_type
        ]