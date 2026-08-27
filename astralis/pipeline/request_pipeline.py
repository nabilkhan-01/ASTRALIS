import os
from pathlib import Path

from astralis.brain.brain import Brain
from astralis.brain.context import BrainContext
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType
from astralis.memory.retriever import MemoryRetriever
from astralis.monitoring.monitor import Monitor


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


class RequestPipeline:
    """Coordinates request processing."""

    def __init__(
        self,
        brain: Brain,
        retriever: MemoryRetriever,
        monitor: Monitor,
    ) -> None:
        self._brain = brain
        self._retriever = retriever
        self._monitor = monitor

    def process(
        self,
        request: Request,
    ) -> Response:
        """Process a request."""

        with self._monitor.measure() as _timer:
            context = self._retriever.retrieve(
                request,
            )

            brain_context = BrainContext(
                request=request,
                context=context,
            )

            response = self._brain.process(
                brain_context,
            )

        return response