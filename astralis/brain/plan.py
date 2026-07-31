from dataclasses import dataclass

from astralis.capability.capability_type import CapabilityType


@dataclass(
    frozen=True,
    slots=True,
)
class Plan:
    """Describes how the Brain intends to process a request."""

    capability: CapabilityType
