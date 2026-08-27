from astralis.brain.request import Request
from astralis.context.context import Context
from astralis.context.relevance import LexicalRelevanceEngine
from astralis.memory.manager import MemoryManager


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
    ) -> Context:
        """Return a Context of entities ranked by relevance to the request.

        Uses lexical overlap between the request text and each
        entity's name + properties. The result is deterministic
        and ordered by relevance (highest first).

        Entities with zero relevance are excluded.
        """
        entities = self._memory.get_all()
        return self._relevance.build_context(
            request_text=request.text,
            entities=entities,
        )
