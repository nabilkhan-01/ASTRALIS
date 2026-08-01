from astralis.brain.request import Request
from astralis.memory.entity import Entity
from astralis.memory.manager import MemoryManager


class MemoryRetriever:
    """Retrieves memory relevant to a request."""

    def __init__(
        self,
        memory: MemoryManager,
    ) -> None:
        self._memory = memory

    def retrieve(
        self,
        request: Request,
    ) -> list[Entity]:
        """Return memory relevant to a request."""

        # Future implementations will perform
        # filtering, ranking, semantic search,
        # and context-aware retrieval.
        _ = request

        return self._memory.get_all()