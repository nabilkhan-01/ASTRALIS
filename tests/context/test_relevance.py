from astralis.context.relevance import LexicalRelevanceEngine
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType


class TestLexicalRelevanceEngine:
    """Tests for the LexicalRelevanceEngine."""

    @staticmethod
    def _engine() -> LexicalRelevanceEngine:
        """Create a relevance engine."""

        return LexicalRelevanceEngine()

    @staticmethod
    def _entity(
        entity_id: str = "e1",
        name: str = "Test Entity",
        properties: dict[str, object] | None = None,
    ) -> Entity:
        """Create a test entity."""

        return Entity(
            id=entity_id,
            type=EntityType.PROJECT,
            name=name,
            properties=properties or {},
        )

    def test_exact_name_match(
        self,
    ) -> None:
        """Exact name matches produce positive relevance."""

        engine = self._engine()
        entity = self._entity(
            name="Architecture Decision",
        )

        score = engine.score_entity(
            "Architecture Decision",
            entity,
        )

        assert score > 0.0
        assert score <= 1.0

    def test_property_match(
        self,
    ) -> None:
        """Matching terms in entity properties produces positive relevance."""

        engine = self._engine()
        entity = self._entity(
            name="Generic Entity",
            properties={
                "description": "database migration instructions",
            },
        )

        score = engine.score_entity(
            "migration",
            entity,
        )

        assert score > 0.0

    def test_name_match_ranks_above_property_match(
        self,
    ) -> None:
        """Name matches receive higher relevance than property-only matches."""

        engine = self._engine()
        name_matched = self._entity(
            entity_id="name_matched",
            name="Pipeline",
            properties={},
        )
        prop_matched = self._entity(
            entity_id="prop_matched",
            name="Other",
            properties={
                "tag": "Pipeline",
            },
        )

        name_score = engine.score_entity(
            "Pipeline",
            name_matched,
        )
        prop_score = engine.score_entity(
            "Pipeline",
            prop_matched,
        )

        assert name_score > prop_score

    def test_unrelated_entity_exclusion(
        self,
    ) -> None:
        """Entities with no overlapping terms are excluded from context."""

        engine = self._engine()
        unrelated = self._entity(
            name="Weather Service",
            properties={
                "city": "London",
            },
        )

        context = engine.build_context(
            "database migration",
            [unrelated],
        )

        assert len(context.items) == 0

    def test_case_normalization(
        self,
    ) -> None:
        """Relevance scoring is case-insensitive."""

        engine = self._engine()
        entity = self._entity(
            name="ASTRALIS Core",
        )

        lower_score = engine.score_entity(
            "astralis core",
            entity,
        )
        upper_score = engine.score_entity(
            "ASTRALIS CORE",
            entity,
        )

        assert lower_score == upper_score
        assert lower_score > 0.0

    def test_stop_word_filtering(
        self,
        ) -> None:
        """Stop words alone do not produce relevance."""

        engine = self._engine()
        entity = self._entity(
            name="ASTRALIS Core",
        )

        score = engine.score_entity(
            "the is at which on and",
            entity,
        )

        assert score == 0.0

    def test_identifier_tokenization(
        self,
    ) -> None:
        """Identifiers in camelCase and snake_case are split into tokens."""

        engine = self._engine()
        camel_entity = self._entity(
            name="MemoryManager",
        )
        snake_entity = self._entity(
            name="request_pipeline",
        )

        camel_score = engine.score_entity(
            "manager",
            camel_entity,
        )
        snake_score = engine.score_entity(
            "pipeline",
            snake_entity,
        )

        assert camel_score > 0.0
        assert snake_score > 0.0

    def test_deterministic_ordering_with_tie_breaker(
        self,
    ) -> None:
        """Entities with equal relevance are ordered deterministically by id."""

        engine = self._engine()
        entity_b = self._entity(
            entity_id="entity_b",
            name="Common Item",
        )
        entity_a = self._entity(
            entity_id="entity_a",
            name="Common Item",
        )

        # Pass in reverse order to verify sorting by entity.id
        context = engine.build_context(
            "Common Item",
            [entity_b, entity_a],
        )

        assert len(context.items) == 2
        assert context.items[0].entity.id == "entity_a"
        assert context.items[1].entity.id == "entity_b"

    def test_empty_result(
        self,
    ) -> None:
        """Empty or whitespace-only queries return an empty context."""

        engine = self._engine()
        entity = self._entity(
            name="Some Entity",
        )

        empty_context = engine.build_context(
            "",
            [entity],
        )
        whitespace_context = engine.build_context(
            "   ",
            [entity],
        )

        assert len(empty_context.items) == 0
        assert len(whitespace_context.items) == 0

    def test_relevance_bounds(
        self,
    ) -> None:
        """Relevance scores always fall strictly within [0.0, 1.0]."""

        engine = self._engine()
        entity = self._entity(
            name="ASTRALIS Memory System",
            properties={
                "description": "ASTRALIS Memory System storage and retrieval",
            },
        )

        # Long query with repeated words
        score = engine.score_entity(
            "ASTRALIS Memory System storage retrieval extra words not found",
            entity,
        )

        assert 0.0 <= score <= 1.0
