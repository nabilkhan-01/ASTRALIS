from dataclasses import dataclass

from astralis.context.context_item import ContextItem


@dataclass(
    frozen=True,
    slots=True,
)
class Context:
    """Represents request-scoped context."""

    items: tuple[ContextItem, ...]
