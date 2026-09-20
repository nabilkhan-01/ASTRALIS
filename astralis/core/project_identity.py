"""Canonical project identity for ASTRALIS.

Defines the permanent, immutable official project identity of ASTRALIS.
This identity is source-controlled and cannot be overridden by mutable runtime
memory, configuration files (.env), environment variables, or filesystem attributes.
"""

from dataclasses import dataclass
from typing import Final


@dataclass(
    frozen=True,
    slots=True,
)
class ProjectIdentity:
    """Canonical, immutable identity of the ASTRALIS project."""

    name: str = "ASTRALIS"
    founder: str = "Nabil Ahmad Khan"

    @property
    def creator(self) -> str:
        """Alias for founder."""
        return self.founder


CANONICAL_PROJECT_IDENTITY: Final[ProjectIdentity] = ProjectIdentity()
