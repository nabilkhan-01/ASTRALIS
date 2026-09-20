"""Lexical relevance engine for ASTRALIS context foundation."""

from __future__ import annotations

import re

from astralis.context.context import Context
from astralis.context.context_item import ContextItem
from astralis.core.project_identity import (
    CANONICAL_PROJECT_IDENTITY,
    ProjectIdentity,
)
from astralis.memory.entity import Entity
from astralis.memory.entity_type import EntityType


class LexicalRelevanceEngine:
    """Deterministic lexical relevance scorer for entities.

    Produces a normalized float score in [0.0, 1.0] per entity based
    on term overlap between the request text and the entity's searchable
    fields (name and properties).

    Matches in entity.name are weighted higher (3x) than matches in
    entity.properties (1x).

    No embeddings, no vector DB, no LLM, no fuzzy search.
    """

    _NAME_WEIGHT: float = 3.0
    _PROPERTY_WEIGHT: float = 1.0

    _IDENTITY_SEMANTIC_TOKENS: frozenset[str] = frozenset({
        "project",
        "founder",
        "creator",
        "created",
        "creation",
        "made",
        "maker",
        "author",
        "built",
        "builder",
        "yourself",
        "self",
        "identity",
    })

    _STOP_WORDS: frozenset[str] = frozenset({
        "a", "an", "the", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "shall", "can",
        "need", "dare", "ought", "used", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through",
        "during", "before", "after", "above", "below", "between",
        "out", "off", "over", "under", "again", "further", "then",
        "once", "here", "there", "when", "where", "why", "how",
        "all", "both", "each", "few", "more", "most", "other",
        "some", "such", "no", "nor", "not", "only", "own", "same",
        "so", "than", "too", "very", "just", "because", "but",
        "and", "or", "if", "while", "about", "it", "its", "this",
        "that", "these", "those", "i", "me", "my", "we", "our",
        "you", "your", "he", "him", "his", "she", "her", "they",
        "them", "their", "what", "which", "who", "whom", "tell",
        "please", "thanks", "thank", "ok", "yes", "yeah",
        "nope", "hey", "hi", "hello", "good",
    })

    _CAMEL_CASE_PATTERN: re.Pattern[str] = re.compile(
        r"(?<=[a-z])(?=[A-Z])",
    )

    @classmethod
    def _split_identifiers(
        cls,
        text: str,
    ) -> str:
        """Expand camelCase and snake_case identifiers."""
        expanded = cls._CAMEL_CASE_PATTERN.sub(
            " ",
            text,
        )
        return expanded.replace(
            "_",
            " ",
        )

    @classmethod
    def _tokenize(
        cls,
        text: str,
    ) -> set[str]:
        """Split text into a set of unique normalized tokens."""
        expanded = cls._split_identifiers(
            text,
        )
        return {
            t
            for t in re.split(
                r"[^a-z0-9]+",
                expanded.lower(),
            )
            if len(t) >= 2 and t not in cls._STOP_WORDS
        }

    def score_entity(
        self,
        request_text: str,
        entity: Entity,
    ) -> float:
        """Score a single entity against the request text.

        Returns a float in [0.0, 1.0] representing lexical relevance.
        """
        query_tokens = self._tokenize(
            request_text,
        )
        if not query_tokens:
            return 0.0

        name_tokens = self._tokenize(
            entity.name,
        )

        prop_tokens: set[str] = set()
        prop_tokens.update(
            self._tokenize(
                str(entity.type.value),
            ),
        )
        if entity.type is EntityType.PROJECT:
            prop_tokens.update(
                self._IDENTITY_SEMANTIC_TOKENS,
            )

        for key, value in entity.properties.items():
            prop_tokens.update(
                self._tokenize(
                    str(key),
                ),
            )
            prop_tokens.update(
                self._tokenize(
                    str(value),
                ),
            )

        name_matches = len(
            query_tokens & name_tokens,
        )
        prop_only_matches = len(
            (query_tokens & prop_tokens) - name_tokens,
        )

        raw_score = (self._NAME_WEIGHT * name_matches) + (
            self._PROPERTY_WEIGHT * prop_only_matches
        )
        max_possible = self._NAME_WEIGHT * len(
            query_tokens,
        )

        normalized = raw_score / max_possible
        return round(
            max(0.0, min(1.0, normalized)),
            4,
        )

    def score_project_identity(
        self,
        request_text: str,
        identity: ProjectIdentity = CANONICAL_PROJECT_IDENTITY,
    ) -> float:
        """Score project identity relevance against the request text.

        Uses term overlap with the canonical project name (3x weight) and
        project identity semantics such as founder/creator/project/self (1x weight).
        Does NOT rely on matching the founder's name, ensuring queries like
        'Who made Astralis?' or 'Who is the founder?' retrieve identity context.
        """
        query_tokens = self._tokenize(
            request_text,
        )
        if not query_tokens:
            return 0.0

        name_tokens = self._tokenize(
            identity.name,
        )
        semantic_tokens = self._IDENTITY_SEMANTIC_TOKENS

        name_matches = len(
            query_tokens & name_tokens,
        )
        semantic_matches = len(
            (query_tokens & semantic_tokens) - name_tokens,
        )

        raw_score = (self._NAME_WEIGHT * name_matches) + (
            self._PROPERTY_WEIGHT * semantic_matches
        )
        max_possible = self._NAME_WEIGHT * len(
            query_tokens,
        )

        normalized = raw_score / max_possible
        return round(
            max(0.0, min(1.0, normalized)),
            4,
        )

    def rank_entities(
        self,
        request_text: str,
        entities: list[Entity],
    ) -> list[ContextItem]:
        """Score and sort entities by relevance, descending.

        Entities with zero relevance are excluded from the result.
        Ties are broken by entity id ascending for determinism.

        Returns a list of ContextItem sorted by relevance (highest first).
        """
        scored: list[ContextItem] = []
        for entity in entities:
            relevance = self.score_entity(
                request_text,
                entity,
            )
            if relevance > 0.0:
                scored.append(
                    ContextItem(
                        entity=entity,
                        relevance=relevance,
                    ),
                )

        scored.sort(
            key=lambda item: (-item.relevance, item.entity.id),
        )
        return scored

    def build_context(
        self,
        request_text: str,
        entities: list[Entity],
        identity: ProjectIdentity = CANONICAL_PROJECT_IDENTITY,
    ) -> Context:
        """Build a Context from entities and canonical project identity."""
        items = self.rank_entities(
            request_text,
            entities,
        )
        identity_relevance = self.score_project_identity(
            request_text=request_text,
            identity=identity,
        )
        return Context(
            items=tuple(items),
            project_identity=identity,
            identity_relevance=identity_relevance,
        )
