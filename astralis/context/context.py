from dataclasses import dataclass

from astralis.context.context_item import ContextItem
from astralis.core.project_identity import (
    CANONICAL_PROJECT_IDENTITY,
    ProjectIdentity,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Context:
    """Represents an ephemeral, request-scoped collection of context items.

    Context is created for a single request and is not intended for
    cross-request reuse, caching, or persistence.
    """

    items: tuple[ContextItem, ...] = ()
    project_identity: ProjectIdentity = CANONICAL_PROJECT_IDENTITY
    identity_relevance: float = 0.0

    @property
    def creator(self) -> str:
        """Return the canonical project creator."""
        return self.project_identity.creator

    @property
    def founder(self) -> str:
        """Return the canonical project founder."""
        return self.project_identity.founder

    @property
    def is_identity_relevant(self) -> bool:
        """Return whether the request is relevant to canonical project identity."""
        return self.identity_relevance > 0.0

    @property
    def has_context(self) -> bool:
        """Return True if any items or relevant project identity are present."""
        return bool(self.items or self.is_identity_relevant)
