from dataclasses import dataclass

from astralis.context.context_item import ContextItem


@dataclass(
    frozen=True,
    slots=True,
)
class Context:
    """Represents an ephemeral, request-scoped collection of context items.

    Context is created for a single request and is not intended for
    cross-request reuse, caching, or persistence.
    """

    items: tuple[ContextItem, ...]
