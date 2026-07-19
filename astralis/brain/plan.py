from dataclasses import dataclass


@dataclass
class ExecutionPlan:
    """Describes how the Brain intends to process a request."""

    provider_required: bool = True
    memory_required: bool = False
    tools_required: bool = False