import os
from pathlib import Path

from astralis.brain.request import Request
from astralis.context.context import Context
from astralis.context.relevance import LexicalRelevanceEngine
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.manager import MemoryManager


def resolve_current_project(
    entities: list[Entity],
    cwd: Path | None = None,
) -> Entity | None:
    """Resolve the PROJECT Entity corresponding to the working directory.

    Matches entities where entity.type is EntityType.PROJECT and the working
    directory is equal to or a descendant of entity.properties['root_path'].

    If multiple projects match, the deepest root path is chosen. Ties are
    broken deterministically by entity.id ascending. If no project matches,
    returns None.
    """

    try:
        resolved_cwd = (cwd if cwd is not None else Path.cwd()).resolve()
    except (ValueError, OSError):
        return None

    norm_cwd = os.path.normcase(
        str(
            resolved_cwd,
        ),
    )

    matches: list[tuple[int, str, Entity]] = []

    for entity in entities:
        if entity.type is not EntityType.PROJECT:
            continue

        root_path_val = entity.properties.get(
            "root_path",
        )

        if not isinstance(
            root_path_val,
            str,
        ) or not root_path_val.strip():
            continue

        try:
            resolved_root = Path(
                root_path_val,
            ).resolve()
        except (ValueError, OSError):
            continue

        norm_root = os.path.normcase(
            str(
                resolved_root,
            ),
        )

        is_match = False

        if norm_cwd == norm_root:
            is_match = True
        else:
            root_prefix = (
                norm_root
                if norm_root.endswith(
                    (os.sep, "/"),
                )
                else norm_root + os.sep
            )

            if norm_cwd.startswith(
                root_prefix,
            ):
                is_match = True

        if is_match:
            depth = len(
                resolved_root.parts,
            )

            matches.append(
                (
                    depth,
                    entity.id,
                    entity,
                ),
            )

    if not matches:
        return None

    matches.sort(
        key=lambda item: (
            -item[0],
            item[1],
        ),
    )

    return matches[0][2]


class MemoryRetriever:
    """Retrieves a request-scoped Context from memory."""

    def __init__(
        self,
        memory: MemoryManager,
        relevance_engine: LexicalRelevanceEngine | None = None,
    ) -> None:
        self._memory = memory
        self._relevance = relevance_engine or LexicalRelevanceEngine()

    def retrieve(
        self,
        request: Request,
        cwd: Path | None = None,
    ) -> Context:
        """Return a Context of entities ranked by relevance to the request.

        Scopes candidate project entities to the active project for the given
        working directory (or Path.cwd()). If a current project is found,
        foreign PROJECT entities are excluded. If no current project is found,
        all entities remain candidates.

        Entities are ranked using deterministic lexical relevance against
        the request text. Entities with zero relevance are excluded.
        """

        entities = self._memory.get_all()

        current_project = resolve_current_project(
            entities=entities,
            cwd=cwd,
        )

        if current_project is not None:
            candidates = [
                entity
                for entity in entities
                if entity.type is not EntityType.PROJECT
                or entity.id == current_project.id
            ]
        else:
            candidates = entities

        return self._relevance.build_context(
            request_text=request.text,
            entities=candidates,
        )
