from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class Provenance:
    """Represents the origin metadata of a persistent entity."""

    source_type: str
    source_identifier: str
