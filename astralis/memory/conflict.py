from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType


@dataclass(
    frozen=True,
    slots=True,
)
class ConflictReport:
    """Describes a structural inconsistency between two DECISION entities.

    entity_a is the newer decision that declares it supersedes entity_b.
    entity_b is the predecessor that is incorrectly still marked active.

    This is detection only. No entity is modified or resolved automatically.
    """

    entity_a: Entity
    entity_b: Entity
    reason: str


def detect_conflicts(
    entities: Sequence[Entity],
) -> list[ConflictReport]:
    """Detect structural conflicts among a sequence of entities.

    Detection rule (v0.4.0):

    A conflict is reported when a DECISION entity A declares:

        properties["supersedes"] = B.id

    and entity B is present in the supplied entities with:

        type == EntityType.DECISION
        properties["status"] == "active"

    A valid supersession (B.status == "superseded") is not reported.
    Missing referenced IDs produce no report.
    Non-DECISION entities are ignored.

    Results are deterministic: sorted by (entity_a.id, entity_b.id).
    This function does not modify any entity.
    """

    decision_by_id = {
        entity.id: entity
        for entity in entities
        if entity.type is EntityType.DECISION
    }

    reports: list[ConflictReport] = []

    for entity_a in decision_by_id.values():
        supersedes_id = entity_a.properties.get("supersedes")

        if not isinstance(supersedes_id, str):
            continue

        entity_b = decision_by_id.get(supersedes_id)

        if entity_b is None:
            continue

        if entity_b.properties.get("status") != "active":
            continue

        reports.append(
            ConflictReport(
                entity_a=entity_a,
                entity_b=entity_b,
                reason=(
                    f"Decision '{entity_a.id}' supersedes '{entity_b.id}'"
                    f" but '{entity_b.id}' is still marked active."
                ),
            ),
        )

    reports.sort(
        key=lambda r: (r.entity_a.id, r.entity_b.id),
    )

    return reports
