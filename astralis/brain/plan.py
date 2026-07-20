from dataclasses import dataclass

from astralis.capability.capability_type import CapabilityType


@dataclass
class ExecutionPlan:
    """Describes how the Brain intends to process a request."""

    capability: CapabilityType